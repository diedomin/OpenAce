from flask import Flask, Response
import requests
import time
import os
import logging
import logging_config

logging_config.configure_logging()

app = Flask("OpenAce")

ACESTREAM_HOST = os.getenv("ACESTREAM_HOST", "127.0.0.1")
ACESTREAM_PORT = os.getenv("ACESTREAM_PORT", "6878")
ACESTREAM_ENGINE = f"http://{ACESTREAM_HOST}:{ACESTREAM_PORT}"

@app.route("/play/<content_id>")
def play(content_id):
    start_url = f"{ACESTREAM_ENGINE}/ace/getstream?content_id={content_id}"
    logging.info(f"Requesting stream: {start_url}")

    for i in range(10):
        try:
            r = requests.get(start_url, stream=True, timeout=(5, 60))
            if r.status_code == 200:
                logging.info(f"✅ Stream available (attempt {i+1})")

                def generate():
                    total_bytes = 0
                    last_log_time = time.time()
                    try:
                        for chunk in r.iter_content(chunk_size=8192):
                            if not chunk:
                                continue

                            yield chunk
                            total_bytes += len(chunk)

                            if total_bytes >= 5*1024*1024 or (time.time() - last_log_time) > 60:
                                logging.info(f"📡 Transmitted {total_bytes / (1024*1024):.2f} MB so far")
                                total_bytes = 0
                                last_log_time = time.time()

                    except requests.exceptions.ReadTimeout:
                        logging.error("❌ Read timeout from AceStream server")
                    except Exception as e:
                        logging.error(f"❌ Unexpected error during transmission: {e}")
                    finally:
                        logging.info("🔌 Transmission with AceStream ended")

                return Response(generate(), content_type='video/mp2t')

            else:
                logging.warning(f"⚠️ Attempt {i+1}: unexpected status code {r.status_code}")

        except Exception as e:
            logging.warning(f"⚠️ Attempt {i+1} failed: {e}")

        time.sleep(1.5)

    logging.error("❌ Stream is not available after 10 attempts")
    return "Stream not available", 503

@app.route("/")
def root():
    logging.info("Application status check.")
    return "OpenAce is running"

if __name__ == "__main__":
    logging.info("🚀 Starting OpenAce")
    app.run(host="0.0.0.0", port=8888)
