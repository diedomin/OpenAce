import logging
from datetime import datetime, timezone

def log_event(level, event, component, **kwargs):
    log_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level.upper(),
        "component": component,
        "event": event,
        **kwargs
    }
    getattr(logging, level.lower())(log_data)
