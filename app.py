from flask import Flask
import config
from blueprints.admin.view import admin_bp
from blueprints.auth.view import auth_bp
from blueprints.blog.views import blog_bp
from extensions import db, login_manager, bootstrap, ckeditor, dropzone
from flask_wtf import CSRFProtect


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(blog_bp)

    db.init_app(app)
    login_manager.init_app(app)
    #bootstrap.init_app(app)
    CSRFProtect(app)
    ckeditor.init_app(app)
    dropzone.init_app(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
