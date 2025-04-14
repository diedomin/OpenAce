from app.routes.play import play_bp
from app.routes.hls import hls_bp
from app.routes.iptv import iptv_bp

def register_blueprints(app):
    app.register_blueprint(play_bp)
    app.register_blueprint(hls_bp)
    app.register_blueprint(iptv_bp)
