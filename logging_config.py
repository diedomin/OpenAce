import logging
import logging.handlers
import os
import sys

LOG_DIR = "/var/log/openace"
LOG_FILE = os.path.join(LOG_DIR, "proxy.log")  # Usamos proxy.log para los logs de la aplicación

os.makedirs(LOG_DIR, exist_ok=True)

def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    # RotatingFileHandler para los logs de la aplicación
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=2
    )
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    # Limpiar los handlers anteriores y configurar los nuevos
    logger.handlers = []
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
