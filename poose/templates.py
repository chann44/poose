from datetime import datetime, timezone
TEMP = """-- Migration created at {ts}

-- +migrate Up
-- Write your UP migration here.
-- Example:
-- CREATE TABLE example (id INTEGER PRIMARY KEY);

-- +migrate Down
-- Write your DOWN migration here.
-- Example:
-- DROP TABLE example;
"""

def render() -> str:
    return TEMP.format(ts=datetime.now(timezone.utc).isoformat())


def version_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")