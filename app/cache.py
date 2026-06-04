"""Async Redis cache manager for sub-10ms response times."""
import json
from typing import Any, Optional
import redis.asyncio as aioredis


class CacheManager:
    """
    Async Redis cache manager.
    
    Strategy:
    - Hot data cached with TTL — sub-10ms reads
    - Write-through caching on events
    - Pub/Sub for real-time event broadcasting
    """

    def __init__(self, client: aioredis.Redis):
        self._client = client

    @classmethod
    async def create(cls, url: str, max_connections: int = 20) -> "CacheManager":
        client = await aioredis.from_url(
            url,
            encoding="utf-8",
            decode_responses=True,
            max_connections=max_connections
        )
        return cls(client)

    async def get(self, key: str) -> Optional[Any]:
        """Get cached value — non-blocking."""
        value = await self._client.get(key)
        return json.loads(value) if value else None

    async def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Set cached value with TTL — non-blocking."""
        await self._client.setex(key, ttl, json.dumps(value))

    async def delete(self, key: str) -> None:
        """Invalidate cache key."""
        await self._client.delete(key)

    async def publish(self, channel: str, message: Any) -> None:
        """Publish event to Pub/Sub channel."""
        await self._client.publish(channel, json.dumps(message))

    async def get_or_set(self, key: str, fetch_fn, ttl: int = 300) -> Any:
        """
        Cache-aside pattern.
        Returns cached value if exists, otherwise fetches and caches.
        """
        cached = await self.get(key)
        if cached is not None:
            return cached
        value = await fetch_fn()
        await self.set(key, value, ttl)
        return value

    async def incr(self, key: str) -> int:
        """Atomic increment — for counters/rate limiting."""
        return await self._client.incr(key)

    async def close(self):
        await self._client.close()
