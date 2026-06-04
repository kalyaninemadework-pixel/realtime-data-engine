"""Events API — async non-blocking endpoints."""
import time
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Any, Optional

router = APIRouter()


class EventPayload(BaseModel):
    type: str
    payload: dict[str, Any]
    source: Optional[str] = "api"


@router.post("/")
async def push_event(event: EventPayload, request: Request):
    """Push a single event into the real-time pipeline."""
    event_data = {
        "type": event.type,
        "payload": event.payload,
        "source": event.source,
        "timestamp": time.time()
    }
    await request.app.state.pipeline.push_event(event_data)
    return {"status": "queued", "event_type": event.type}


@router.post("/batch")
async def push_batch(events: list[EventPayload], request: Request):
    """
    Batch event ingestion — high throughput endpoint.
    Processes up to 1000 events per request.
    """
    if len(events) > 1000:
        raise HTTPException(400, "Batch size exceeds limit of 1000")

    for event in events:
        await request.app.state.pipeline.push_event({
            "type": event.type,
            "payload": event.payload,
            "source": event.source,
            "timestamp": time.time()
        })
    return {"status": "queued", "count": len(events)}


@router.get("/recent")
async def get_recent_events(request: Request, limit: int = 20):
    """Fetch recent events — cached for sub-10ms response."""
    cache_key = f"events:recent:{limit}"
    cached = await request.app.state.cache.get(cache_key)
    if cached:
        return {"events": cached, "source": "cache"}

    events = await request.app.state.db.fetch_all(
        "SELECT * FROM events ORDER BY timestamp DESC LIMIT $1", limit
    )
    await request.app.state.cache.set(cache_key, events, ttl=10)
    return {"events": events, "source": "database"}
