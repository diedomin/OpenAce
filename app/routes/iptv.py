from flask import Blueprint, current_app, Response, request
import requests
from app.utils.logging_utils import log_event

iptv_bp = Blueprint('iptv', __name__, url_prefix='/iptv')
COMPONENT = "iptv_proxy"

@iptv_bp.route('/<seg1>/<seg2>/<seg3>', methods=['GET', 'HEAD'])
def iptv_proxy(seg1, seg2, seg3):
    servers = current_app.config.get("IPTV_SERVERS", [])
    if not servers:
        log_event("error", "iptv_proxy_error", COMPONENT, error="No IPTV servers configured")
        return Response("No IPTV servers configured", status=500)

    last_error = None
    # Obtiene el User-Agent de la solicitud, o usa uno por defecto
    ua = request.headers.get("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    custom_headers = {"User-Agent": ua}

    for server in servers:
        server = server.strip()
        remote_url = f"http://{server}/{seg1}/{seg2}/{seg3}"
        log_event("info", "iptv_stream_attempt", COMPONENT, remote_url=remote_url)
        try:
            # Se agrega el encabezado User-Agent en la petición
            r = requests.get(remote_url, stream=True, timeout=5, headers=custom_headers)
            r.raise_for_status()
            log_event("info", "iptv_stream_started", COMPONENT, remote_url=remote_url, status_code=r.status_code)

            # Obtener todos los encabezados del servidor remoto
            headers = dict(r.headers)

            # Si es una solicitud HEAD, regresamos solo los encabezados con el estado correcto.
            if request.method == "HEAD":
                return Response(status=r.status_code, headers=headers)

            # Para GET, devolvemos el contenido en streaming
            return Response(r.iter_content(chunk_size=1024),
                            status=r.status_code,
                            headers=headers,
                            direct_passthrough=True)
        except requests.exceptions.RequestException as e:
            last_error = e
            log_event("warning", "iptv_stream_failed", COMPONENT, remote_url=remote_url, error=str(e))

    log_event("error", "iptv_all_servers_failed", COMPONENT, error=str(last_error))
    return Response("Failed to fetch IPTV stream from all servers", status=503)
