# Contributing to Real-Time Data Engine

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)
- [Performance Considerations](#performance-considerations)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and constructive in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/realtime-data-engine.git
   cd realtime-data-engine
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/kalyaninemadework-pixel/realtime-data-engine.git
   ```

## Development Setup

### Prerequisites
- Docker & Docker Compose v2+
- Python 3.11+
- Git

### Local Environment

1. **Copy environment template**:
   ```bash
   cp .env.example .env
   ```

2. **Start all services**:
   ```bash
   docker compose up --build
   ```

3. **Access the application**:
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines

3. **Test your changes**:
   ```bash
   pytest tests/ -v --cov=app
   ```

### Code Style Guidelines

- **Python**: Follow PEP 8 style guide
- **Async**: Use `async`/`await` for all I/O operations
- **Type hints**: Use Python type hints in function signatures
- **Docstrings**: Add docstrings to all functions and classes
- **Naming**: Use descriptive, clear names

Example:
```python
async def push_event(
    event: EventPayload,
    pipeline: DataPipeline
) -> EventResponse:
    """
    Push a new event to the data pipeline.
    
    Args:
        event: Event payload containing type and data
        pipeline: Data pipeline instance
        
    Returns:
        EventResponse with status and event ID
        
    Raises:
        ValueError: If event validation fails
    """
```

## Commit Guidelines

Follow the conventional commit format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: A new feature
- `fix`: A bug fix
- `perf`: Performance improvements
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Test additions or updates

### Examples
```
perf(pipeline): optimize query batching for 35% improvement
feat(async): add asyncio event queue with batch flushing
fix(cache): resolve Redis connection pool deadlock
```

## Pull Request Process

1. **Update your fork**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push your changes**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request** with:
   - Clear title describing the change
   - Performance benchmarks (if applicable)
   - Test results

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run async tests
pytest tests/ -v -m asyncio

# Performance test
python benchmarks/benchmark.py
```

### Performance Requirements

All PRs must maintain or improve:
- ✅ Sub-10ms response time
- ✅ 35% throughput improvement
- ✅ Zero DB deadlocks

### Benchmarking

Document performance metrics:
```python
# Before optimization
Response time: 15ms
Throughput: 100 events/sec

# After optimization
Response time: 9ms (40% improvement)
Throughput: 140 events/sec (40% improvement)
```

## Performance Considerations

- ✅ Use AsyncIO for all I/O
- ✅ Implement connection pooling
- ✅ Use Redis caching with TTL
- ✅ Batch queries when possible
- ✅ Profile performance-critical code
- ✅ Add metrics and monitoring

Example:
```python
async def get_or_set(
    key: str,
    fetch_fn,
    ttl: int = 300
) -> Any:
    """Cache-aside pattern with TTL."""
    cached = await redis.get(key)
    if cached:
        return json.loads(cached)  # Sub-10ms
    
    value = await fetch_fn()  # DB fetch only on miss
    await redis.set(key, json.dumps(value), ttl)
    return value
```

## Documentation

- Update README.md if adding new features
- Add docstrings to all functions
- Include architecture diagrams
- Document API endpoints
- Add performance benchmarks

## Security Guidelines

- Never commit secrets or API keys
- Use environment variables for sensitive data
- Validate all inputs
- Use parameterized queries
- Add rate limiting

## Questions or Issues?

- Open a GitHub issue for bugs
- Use Discussions for questions
- Email: kalyani.nemade.work@gmail.com

---

**Thank you for contributing! 🎉**

We appreciate your effort in making this project faster and better!
