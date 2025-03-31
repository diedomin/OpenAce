from flask import Blueprint, Response, current_app, request
import requests
import re
from app.utils.logging_utils import log_event

hls_bp = Blueprint('hls', __name__, url_prefix='/hls')
COMPONENT = "hls_proxy"

@hls_bp.route('/<content_id>', defaults={'subpath': 'manifest.m3u8'})
@hls_bp.route('/<content_id>/<path:subpath>')
def hls_proxy(content_id, subpath):
    host = current_app.config.get("ACESTREAM_HOST", "127.0.0.1")
    port = current_app.config.get("ACESTREAM_PORT", "6878")

    try:
        if subpath == "manifest.m3u8":
            ace_url = f"http://{host}:{port}/ace/manifest.m3u8?id={content_id}"
            r = requests.get(ace_url, timeout=5)
            r.raise_for_status()

            modified_content = re.sub(
                r'([a-zA-Z0-9_\-]+\.m3u8)',
                rf'/hls/{content_id}/\1',
                r.text
            )

            log_event("info", "hls_manifest_fetched", COMPONENT, content_id=content_id, source_url=ace_url, status="success")
            return Response(modified_content, content_type='application/vnd.apple.mpegurl')

        else:
            ace_url = f"http://{host}:{port}/ace/{subpath}?id={content_id}"
            r = requests.get(ace_url, stream=True, timeout=5)
            r.raise_for_status()

            log_event("info", "hls_segment_fetched", COMPONENT, content_id=content_id, segment=subpath, source_url=ace_url, status="success")
            return Response(r.iter_content(chunk_size=1024), content_type=r.headers.get('Content-Type'))

    except requests.exceptions.RequestException as e:
        log_event("error", "hls_proxy_error", COMPONENT, content_id=content_id, subpath=subpath, error=str(e), status="connection_failed")
        return Response("Failed to connect to AceStream engine", status=503)
