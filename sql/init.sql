-- Initialize database schema for Real-Time Data Engine

CREATE TABLE IF NOT EXISTS events (
    id          BIGSERIAL PRIMARY KEY,
    type        VARCHAR(100) NOT NULL,
    payload     JSONB,
    source      VARCHAR(100) DEFAULT 'api',
    timestamp   DOUBLE PRECISION NOT NULL,
    processed   BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for high-throughput queries
CREATE INDEX IF NOT EXISTS idx_events_type      ON events(type);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_events_processed ON events(processed);
CREATE INDEX IF NOT EXISTS idx_events_payload   ON events USING GIN(payload);

-- Metrics table
CREATE TABLE IF NOT EXISTS metrics (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    value       BIGINT DEFAULT 0,
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);
