from flask import Flask
from config import Config
from .models import db
from flask_bootstrap import Bootstrap
def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    app.config.from_object(Config)
    app.config['STATIC_FOLDER'] = '/fooddrive/static'
    db.init_app(app)
    from .views.root import root
    app.register_blueprint(root)
    return app