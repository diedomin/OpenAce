import logging
from app import create_app

logging.info("Starting OpenAce")
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
