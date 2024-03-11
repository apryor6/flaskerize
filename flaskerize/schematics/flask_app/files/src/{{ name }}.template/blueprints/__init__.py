def register_routes(app, api):
    from .home import blueprint as home_bp
    from .status import blueprint as status_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(status_bp)
