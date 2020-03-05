from datetime import timedelta
import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))



SECRET_KEY = '12345678'
TEMPLATES_AUTI_RELODE = True
SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)

#ckeditor
CKEDITOR_ENABLE_CSRF = True
CKEDITOR_FILE_UPLOADER = 'admin.upload_image'
add_path = 'blog/static/uploads'
BLOG_UPLOAD_PATH = os.path.join(basedir, add_path)
BLOG_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
BLOG_ALLOWED_MOVIE_EXTENSIONS = ['mp4', 'mov']


#数据库
DB_USERNAME = 'root'
DB_PASSWORD = '****'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'blog'

DB_URI = 'mysql://%s:%s@%s:%s/%s' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

#Dropzone配置
# DROPZONE_ALLOWED_FILE_CUSOM = True
# DROPZONE_ALLOWED_FILE_TYPE = 'image'
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # file size exceed to 3 Mb will return a 413 error response.
DROPZONE_MAX_FILE_SIZE = 20
DROPZONE_MAX_FILES = 30
DROPZONE_ENABLE_CSRF = True

ALBUMY_UPLOAD_PATH = os.path.join(basedir + '/blog/static/', 'Album')
PHOTO_UPLOAD_PATH = os.path.join(basedir + '/blog/static/', 'Photo')
VLOG_UPLOAD_PATH = os.path.join(basedir + '/blog/static/', 'Vlog')
CC_BLOG_UPLOAD_PATH = os.path.join(basedir + '/blog/static/', 'CC_blog')
JOURNAL_UPLOAD_PATH = os.path.join(basedir + '/blog/static/', 'Journal')


