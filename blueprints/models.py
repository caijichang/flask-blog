from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from sqlalchemy.event import listens_for
import os

#管理员
class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20))
    _password = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)


#77's博客文章
class PostSeven(db.Model):
    __tablename__ = 'post_seven'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow(), index=True)


#CC's博客分类
class CategoryCc(db.Model):
    __tablename__ = 'category_cc'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)

    posts_cc = db.relationship('PostCc', back_populates='category_cc', cascade='all')

    def delete(self):
        db.session.delete(self)
        db.session.commit()

#CC's博客文章
class PostCc(db.Model):
    __tablename__ = 'post_cc'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    filename = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow(), index=True)

    category_cc_id = db.Column(db.Integer, db.ForeignKey('category_cc.id'))
    category_cc = db.relationship('CategoryCc', back_populates='posts_cc')

@listens_for(PostCc.filename, 'set')
def remove_post_cc(target, value, oldvalue, initiator):
    if isinstance(oldvalue, str):
        path = '/Users/caijichang/PycharmProjects/cms_blog/static/' + oldvalue
        os.remove(path)

#life文章
class Post_life(db.Model):
    __tablename__ = 'post_life'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow(), index=True)


#journal的文章
class Post_journal(db.Model):
    __tablename__ = 'post_journal'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    filename = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow(), index=True)

@listens_for(Post_journal.filename, 'set')
def remove_post_journal(target, value, oldvalue, initiator):
    if isinstance(oldvalue, str):
        path = '/Users/caijichang/PycharmProjects/cms_blog/static/' + oldvalue
        os.remove(path)

#Album
class Album(db.Model):
    __tablename__ = 'album'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(500))
    filename = db.Column(db.String(64))
    filename_small = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    photos = db.relationship('Photo', back_populates='album', cascade='all')

    def delete(self):
        db.session.delete(self)
        db.session.commit()


@listens_for(Album.filename, 'set')
def remove_album_photo(target, value, oldvalue, initiator):
    if isinstance(oldvalue, str):
        path = '/Users/caijichang/PycharmProjects/cms_blog/static/' + oldvalue
        os.remove(path)
@listens_for(Album.filename_small, 'set')
def remove_album_photo(target, value, oldvalue, initiator):
    if isinstance(oldvalue, str):
        path = '/Users/caijichang/PycharmProjects/cms_blog/static/' + oldvalue
        if os.path.exists(path):
            os.remove(path)

# photo
class Photo(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(64))
    filename_small = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    album = db.relationship('Album', back_populates='photos')

#vlog
class Vlog(db.Model):
    __tablename__ = 'vlog'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(500))
    filename = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@listens_for(Vlog.filename, 'set')
def remove_vlog(target, value, oldvalue, initiator):
    if isinstance(oldvalue, str):
        path = '/Users/caijichang/PycharmProjects/cms_blog/static/' + oldvalue
        os.remove(path)





