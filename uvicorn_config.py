import os

host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", 8000))
log_level = os.getenv("LOG_LEVEL", "info")
workers = int(os.getenv("WORKERS", 4))

config = {
    "host": host,
    "port": port,
    "log_level": log_level,
    "workers": workers,
}