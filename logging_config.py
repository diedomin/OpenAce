import logging
import logging.handlers
import os
import sys
from pythonjsonlogger import jsonlogger

LOG_DIR = "/var/log/openace"
LOG_FILE = os.path.join(LOG_DIR, "proxy.log")

os.makedirs(LOG_DIR, exist_ok=True)

def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Json format for logs
    log_format = '%(asctime)s %(levelname)s %(name)s %(message)s'
    json_formatter = jsonlogger.JsonFormatter(log_format)

    # RotatingFileHandler
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=2
    )
    file_handler.setFormatter(json_formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(json_formatter)

    logger.handlers = []
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
