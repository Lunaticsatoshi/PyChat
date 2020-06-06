from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')


    with app.app_context():
        #Importing
        from .routes import routing
        from .filters import _slice
        from .database import DataBase

        #Registering The Routes
        app.register_blueprint(routing, url_prefix = "/")

        #Registering Context
        @app.context_processor
        def slice():
            return dict(slice= _slice)

        return app