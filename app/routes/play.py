import time
import requests
from flask import Blueprint, Response, current_app
from app.utils.logging_utils import log_event

play_bp = Blueprint('play', __name__, url_prefix='/play')
COMPONENT = "play_proxy"

@play_bp.route('/<content_id>')
def play(content_id):
    start_url = f"{current_app.config['ACESTREAM_ENGINE']}/ace/getstream?content_id={content_id}"
    log_event("info", "stream_request_started", COMPONENT, content_id=content_id, source_url=start_url)

    for i in range(10):
        try:
            r = requests.get(start_url, stream=True, timeout=(5, 60))
            if r.status_code == 200:
                log_event("info", "stream_available", COMPONENT, content_id=content_id, attempt=i+1, status_code=r.status_code)

                def generate():
                    total_bytes = 0
                    last_log_time = time.time()
                    try:
                        for chunk in r.iter_content(chunk_size=8192):
                            if not chunk:
                                continue
                            yield chunk
                            total_bytes += len(chunk)
                            now = time.time()

                            if total_bytes >= 5 * 1024 * 1024 or (now - last_log_time) > 60:
                                mb = round(total_bytes / (1024 * 1024), 2)
                                log_event("info", "stream_progress", COMPONENT, content_id=content_id, bytes_transmitted_mb=mb)
                                total_bytes = 0
                                last_log_time = now
                    except requests.exceptions.ReadTimeout:
                        log_event("error", "stream_read_timeout", COMPONENT, content_id=content_id, error="Read timeout from AceStream")
                    except Exception as e:
                        log_event("error", "stream_transmission_error", COMPONENT, content_id=content_id, error=str(e))
                    finally:
                        log_event("info", "stream_transmission_ended", COMPONENT, content_id=content_id)

                return Response(generate(), content_type='video/mp2t')
            else:
                log_event("warning", "stream_unexpected_status", COMPONENT, content_id=content_id, attempt=i+1, status_code=r.status_code)
        except Exception as e:
            log_event("warning", "stream_attempt_failed", COMPONENT, content_id=content_id, attempt=i+1, error=str(e))
        time.sleep(1.5)

    log_event("error", "stream_unavailable", COMPONENT, content_id=content_id, attempts=10)
    return "Stream not available", 503
