from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_dropzone import Dropzone

db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()
ckeditor = CKEditor()
dropzone = Dropzone()

@login_manager.user_loader
def load_user(user_id):
    from blueprints.models import Admin
    user = Admin.query.get(int(user_id))
    return user


#定义flash消息
login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'
