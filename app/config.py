import os

class Config:
    ACESTREAM_HOST = os.getenv("ACESTREAM_HOST", "127.0.0.1")
    ACESTREAM_PORT = os.getenv("ACESTREAM_PORT", "6878")
    ACESTREAM_ENGINE = f"http://{ACESTREAM_HOST}:{ACESTREAM_PORT}"
