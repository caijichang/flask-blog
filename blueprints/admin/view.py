from flask import render_template, Blueprint, request, redirect, url_for, send_from_directory, current_app
from flask_login import login_required
from blueprints.models import PostSeven, PostCc, CategoryCc, Post_life, Post_journal, Photo, \
    Album, Vlog
from extensions import db
from blueprints.admin.forms import PostSevenForm, PostCCForm, CategoryCCForm, \
    PostLifeForm, PostJournalForm, AlbumForm, VlogForm
from flask_ckeditor import upload_success, upload_fail
from flask_dropzone import random_filename
from utils import allowed_file_image, allowed_file_movie, random_filename_uuid, confirm_folder, resize_image

import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/index/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('admin/index.html')


'''
***************
77的博客
***************
'''
@admin_bp.route('/77_manage_post/', methods=['GET', 'POST'])
@login_required
def seven_manage_post():
    pagination = PostSeven.query.order_by(PostSeven.timestamp.desc()).paginate(
        1, per_page=PostSeven.query.count())
    posts = pagination.items
    return render_template("admin/77's_Blog/77_manage_post.html", pagination=pagination, posts=posts)

@admin_bp.route('/77_manage_post/new/', methods=['GET', 'POST'])
@login_required
def seven_new_post():
    form = PostSevenForm()
    if form.validate_on_submit():
        body = form.body.data
        post = PostSeven(body=body)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('admin.seven_manage_post'))
    return render_template("admin/77's_Blog/77_new_post.html", form=form)

@admin_bp.route('/77_manage_post/<int:post_id>/edit/', methods=['GET', 'POST'])
@login_required
def seven_edit_post(post_id):
    form = PostSevenForm()
    post = PostSeven.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.commit()
        return redirect(url_for('admin.seven_manage_post'))
    form.body.data = post.body
    return render_template("admin/77's_Blog/77_edit_post.html", form=form)

@admin_bp.route('/77_manage_post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def seven_delete_post(post_id):
    post = PostSeven.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('admin.seven_manage_post'))


'''
***************
cc的博客
***************
'''
@admin_bp.route('/CC_manage_post/', methods=['GET', 'POST'])
@login_required
def cc_manage_post():
    pagination = PostCc.query.order_by(PostCc.timestamp.desc()).paginate(
        1, per_page=PostCc.query.count())
    posts = pagination.items
    return render_template("admin/CC's_Blog/CC_manage_post.html", pagination=pagination, posts=posts)

@admin_bp.route('/CC_manage_post/new/', methods=['GET', 'POST'])
@login_required
def cc_new_post():
    form = PostCCForm()
    if form.validate_on_submit():
        try:
            title = form.title.data
            body = form.body.data
            category = CategoryCc.query.get(form.category.data)
            if form.photo.data:
                f = form.photo.data
                filename = random_filename_uuid(f.filename)
                f.save(os.path.join(current_app.config['CC_BLOG_UPLOAD_PATH'], filename))
                filename = 'CC_blog/' + filename
                post = PostCc(title=title, body=body, category_cc=category, filename=filename)
            else:
                post = PostCc(title=title, body=body, category_cc=category)
            db.session.add(post)
            db.session.commit()
        except:
            os.remove(os.path.join('/Users/caijichang/PycharmProjects/cms_blog/static', filename))
            raise TypeError
        return redirect(url_for('admin.cc_manage_post'))
    return render_template("admin/CC's_Blog/CC_new_post.html", form=form)

@admin_bp.route('/CC_manage_post/<int:post_id>/edit/', methods=['GET', 'POST'])
@login_required
def cc_edit_post(post_id):
    form = PostCCForm()
    post = PostCc.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category_cc = CategoryCc.query.get(form.category.data)
        if form.photo.data:
            f = form.photo.data
            filename = random_filename_uuid(f.filename)
            f.save(os.path.join(current_app.config['CC_BLOG_UPLOAD_PATH'], filename))
            filename = 'CC_blog/' + filename
            post.filename = filename
        db.session.commit()
        return redirect(url_for('admin.cc_manage_post'))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_cc_id
    return render_template("admin/CC's_Blog/CC_edit_post.html", form=form)

@admin_bp.route('/CC_manage_post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def cc_delete_post(post_id):
    post = PostCc.query.get_or_404(post_id)
    remove_file = '/Users/caijichang/PycharmProjects/cms_blog/static/' + post.filename
    db.session.delete(post)
    db.session.commit()
    os.remove(remove_file)
    return redirect(url_for('admin.cc_manage_post'))

@admin_bp.route('/CC_manage_category/', methods=['GET', 'POST'])
@login_required
def cc_manage_category():
    pagination = CategoryCc.query.order_by().paginate(
        1, per_page=CategoryCc.query.count())
    categorys = pagination.items
    return render_template("admin/CC's_Blog/CC_manage_category.html", pagination=pagination, categorys=categorys)

@admin_bp.route('/CC_manage_category/new/', methods=['GET', 'POST'])
@login_required
def cc_new_category():
    form = CategoryCCForm()
    if form.validate_on_submit():
        name = form.name.data
        category = CategoryCc(name=name)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('admin.cc_manage_category'))
    return render_template("admin/CC's_Blog/CC_new_category.html", form=form)

@admin_bp.route('/CC_manage_category/<int:category_id>/edit/', methods=['GET', 'POST'])
@login_required
def cc_edit_category(category_id):
    form = CategoryCCForm()
    category = CategoryCc.query.get_or_404(category_id)
    if category.id == 1:
        return redirect(url_for('admin.cc_manage_category'))
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        return redirect(url_for('admin.cc_manage_category'))
    form.name.data = category.name
    return render_template("admin/CC's_Blog/CC_edit_category.html", form=form)

@admin_bp.route('/CC_manage_category/<int:category_id>/delete/', methods=['GET', 'POST'])
@login_required
def cc_delete_category(category_id):
    category = CategoryCc.query.get_or_404(category_id)
    if category.id == 1:
        return redirect(url_for('admin.cc_manage_category'))
    category.delete()
    return redirect(url_for('admin.cc_manage_category'))


'''
***************
Life板块
***************
'''
@admin_bp.route('/Life_manage_post/', methods=['GET', 'POST'])
@login_required
def life_manage_post():
    pagination = Post_life.query.order_by().paginate(
        1, per_page=Post_life.query.count())
    posts = pagination.items
    return render_template("admin/Life/life_manage_post.html", pagination=pagination, posts=posts)

@admin_bp.route('/Life_manage_post/new/', methods=['GET', 'POST'])
@login_required
def life_new_post():
    form = PostLifeForm()
    if form.validate_on_submit():
        body = form.body.data
        post = Post_life(body=body)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('admin.life_manage_post'))
    return render_template("admin/Life/life_new_post.html", form=form)

@admin_bp.route('/Life_manage_post/<int:post_id>/edit/', methods=['GET', 'POST'])
@login_required
def life_edit_post(post_id):
    form = PostLifeForm()
    post = Post_life.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.commit()
        return redirect(url_for('admin.life_manage_post'))
    form.body.data = post.body
    return render_template("admin/Life/life_edit_post.html", form=form)

@admin_bp.route('/Life_manage_post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def life_delete_post(post_id):
    post = Post_life.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('admin.life_manage_post'))


'''
***************
Journal板块
***************
'''
@admin_bp.route('/Journal_manage_post/', methods=['GET', 'POST'])
@login_required
def journal_manage_post():
    pagination = Post_journal.query.order_by().paginate(
        1, per_page=Post_journal.query.count())
    posts = pagination.items
    return render_template("admin/Journal/journal_manage_post.html", pagination=pagination, posts=posts)

@admin_bp.route('/Journal_manage_post/new/', methods=['GET', 'POST'])
@login_required
def journal_new_post():
    form = PostJournalForm()
    if form.validate_on_submit():
        try:
            title = form.title.data
            body = form.body.data
            if form.photo.data:
                f = form.photo.data
                filename = random_filename_uuid(f.filename)
                f.save(os.path.join(current_app.config['JOURNAL_UPLOAD_PATH'], filename))
                filename = 'Journal/' + filename
                post = Post_journal(title=title, body=body, filename=filename)
            else:
                post = Post_journal(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except:
            s.remove(os.path.join('/Users/caijichang/PycharmProjects/cms_blog/static', filename))
            raise TypeError
        return redirect(url_for('admin.journal_manage_post'))
    return render_template("admin/Journal/journal_new_post.html", form=form)

@admin_bp.route('/Journal_manage_post/<int:post_id>/edit/', methods=['GET', 'POST'])
@login_required
def journal_edit_post(post_id):
    form = PostJournalForm()
    post = Post_journal.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        if form.photo.data:
            f = form.photo.data
            filename = random_filename_uuid(f.filename)
            f.save(os.path.join(current_app.config['JOURNAL_UPLOAD_PATH'], filename))
            filename = 'Journal/' + filename
            post.filename = filename
        db.session.commit()
        return redirect(url_for('admin.journal_manage_post'))
    form.title.data = post.title
    form.body.data = post.body
    return render_template("admin/Journal/journal_edit_post.html", form=form)

@admin_bp.route('/Journal_manage_post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def journal_delete_post(post_id):
    post = Post_journal.query.get_or_404(post_id)
    remove_file = '/Users/caijichang/PycharmProjects/cms_blog/static/' + post.filename
    db.session.delete(post)
    db.session.commit()
    os.remove(remove_file)
    return redirect(url_for('admin.journal_manage_post'))


'''
***************
ckeditor上传功能
***************
'''
@admin_bp.route('/uploads/<path:filename>/')
def get_image(filename):
    return send_from_directory(current_app.config['BLOG_UPLOAD_PATH'], filename)

@admin_bp.route('/upload/', methods=['POST'])
def upload_image():
    f = request.files.get('upload')
    if allowed_file_movie(f.filename):
        f.save(os.path.join(current_app.config['BLOG_UPLOAD_PATH'], f.filename))
        url = url_for('admin.get_image', filename=f.filename)
        return upload_success(url, f.filename)
    elif not allowed_file_image(f.filename):
        return upload_fail('Image only!')
    else:
        f.save(os.path.join(current_app.config['BLOG_UPLOAD_PATH'], f.filename))
        url = url_for('admin.get_image', filename=f.filename)
        return upload_success(url, f.filename)


'''
***************
Album
***************
'''
@admin_bp.route('/Album/', methods=['GET', 'POST'])
@login_required
def manage_album():
    pagination = Album.query.order_by().paginate(
        1, per_page=Album.query.count())
    albums = pagination.items
    return render_template('admin/Album/Album.html', pagination=pagination, albums=albums)

@admin_bp.route('/Album/new_album/', methods=['GET', 'POST'])
@login_required
def new_album():
    form = AlbumForm()
    if form.validate_on_submit():
        try:
            name = form.name.data
            description = form.description.data
            f = form.photo.data
            filename = random_filename_uuid(f.filename)
            f.save(os.path.join(current_app.config['ALBUMY_UPLOAD_PATH'], filename))
            filename = 'Album/' + filename
            filename_small = resize_image(f, filename)
            print(filename_small)
            album = Album(name=name, description=description, filename=filename, filename_small=filename_small)
            db.session.add(album)
            db.session.commit()
        except:
            os.remove(os.path.join('/Users/caijichang/PycharmProjects/cms_blog/static', filename))
            if os.path.exists(os.path.join('/Users/caijichang/PycharmProjects/cms_blog/static', filename_small)):
                os.remove(os.path.join('/Users/caijichang/PycharmProjects/cms_blog/static', filename_small))
            raise TypeError
        return redirect(url_for('admin.manage_album'))
    return render_template('admin/Album/new_album.html', form=form)

@admin_bp.route('/Album/<int:album_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_album(album_id):
    form = AlbumForm()
    album = Album.query.get_or_404(album_id)
    if form.validate_on_submit():
        album.name = form.name.data
        album.description = form.description.data
        if form.photo.data:
            f = form.photo.data
            filename = random_filename_uuid(f.filename)
            f.save(os.path.join(current_app.config['ALBUMY_UPLOAD_PATH'], filename))
            filename = 'Album/' + filename
            filename_small = resize_image(f, filename)
            album.filename = filename
            album.filename_small = filename_small
        db.session.commit()
        return redirect(url_for('admin.manage_album'))
    form.name.data = album.name
    form.description.data = album.description
    return render_template("admin/Album/edit_album.html", form=form)

@admin_bp.route('/Album/<int:album_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_album(album_id):
    album = Album.query.get_or_404(album_id)
    remove_file = '/Users/caijichang/PycharmProjects/cms_blog/static/' + album.filename
    remove_file_small = '/Users/caijichang/PycharmProjects/cms_blog/static/' + album.filename_small
    album.delete()
    if os.path.exists(remove_file_small):
        os.remove(remove_file_small)
    if os.path.exists(remove_file):
        os.remove(remove_file)
    return redirect(url_for('admin.manage_album'))

@admin_bp.route('/Album/photo/<int:album_id>', methods=['GET', 'POST'])
@login_required
def manage_photo(album_id):
    pagination = Photo.query.filter_by(album_id=album_id).paginate(
        1, per_page=Photo.query.filter_by(album_id=album_id).count())
    photos = pagination.items
    path = '/static/Photo/'
    return render_template('admin/Album/manage_photo.html', pagination=pagination, photos=photos, album_id=album_id, path=path)

@admin_bp.route('/Album/photo/<int:album_id>/new_photo/', methods=['GET', 'POST'])
@login_required
def new_photo(album_id):
    if request.method == 'POST' and 'file' in request.files:
        f = request.files.get('file')
        filename = random_filename(f.filename)
        album_name = Album.query.get(album_id)
        folder = os.path.join(current_app.config['PHOTO_UPLOAD_PATH'], album_name.name)
        confirm_folder(folder)
        path = os.path.join(folder, filename)
        f.save(path)
        album = Album.query.get(album_id)
        filename = 'Photo' + '/' + album_name.name + '/' + filename
        filename_small = resize_image(f, filename)
        photo = Photo(filename=filename, album=album, filename_small=filename_small)
        db.session.add(photo)
        db.session.commit()
    return render_template('admin/Album/new_photo.html', album_id=album_id)

@admin_bp.route('/Album/photo/<int:photo_id>/delete_photo/', methods=['GET', 'POST'])
@login_required
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    remove_file = '/Users/caijichang/PycharmProjects/cms_blog/static/Photo/' + photo.filename
    remove_file_small = '/Users/caijichang/PycharmProjects/cms_blog/static/Photo/' + photo.filename_small
    db.session.delete(photo)
    db.session.commit()
    if os.path.exists(remove_file_small):
        os.remove(remove_file_small)
    os.remove(remove_file)
    return redirect(url_for('admin.manage_photo', album_id=photo.album_id))


'''
***************
Vlog
***************
'''
@admin_bp.route('/Vlog_manage/', methods=['GET', 'POST'])
@login_required
def manage_vlog():
    pagination = Vlog.query.order_by().paginate(
        1, per_page=Vlog.query.count())
    vlogs = pagination.items
    return render_template('admin/Vlog/manage_vlog.html', pagination=pagination, vlogs=vlogs)

@admin_bp.route('/Vlog/new_vlog/', methods=['GET', 'POST'])
@login_required
def new_vlog():
    form = VlogForm()
    if form.validate_on_submit():
        try:
            name = form.name.data
            description = form.description.data
            f = form.vlog.data
            filename = random_filename_uuid(f.filename)
            f.save(os.path.join(current_app.config['VLOG_UPLOAD_PATH'], filename))
            filename = 'Vlog/' + filename
            vlog = Vlog(name=name, description=description, filename=filename)
            db.session.add(vlog)
            db.session.commit()
        except:
            os.remove(os.path.join('/Users/caijichang/PycharmProjects/cms_blog/static', filename))
            raise TypeError
        return redirect(url_for('admin.manage_vlog'))
    return render_template('admin/Vlog/new_vlog.html', form=form)

@admin_bp.route('/Vlog/<int:vlog_id>/edit_vlog/', methods=['GET', 'POST'])
def edit_vlog(vlog_id):
    form = VlogForm()
    vlog = Vlog.query.get_or_404(vlog_id)
    if form.validate_on_submit():
        vlog.name = form.name.data
        vlog.description = form.description.data
        if form.vlog.data:
            f = form.vlog.data
            filename = random_filename_uuid(f.filename)
            f.save(os.path.join(current_app.config['VLOG_UPLOAD_PATH'], filename))
            filename = 'Vlog/' + filename
            vlog.filename = filename
        db.session.commit()
        return redirect(url_for('admin.manage_vlog'))
    form.name.data = vlog.name
    form.description.data = vlog.description
    if form.vlog.data:
        form.vlog.data = vlog.filename
    return render_template("admin/Vlog/edit_vlog.html", form=form)

@admin_bp.route('/Vlog/<int:vlog_id>/delete_vlog', methods=['GET', 'POST'])
def delete_vlog(vlog_id):
    vlog = Vlog.query.get_or_404(vlog_id)
    remove_file = '/Users/caijichang/PycharmProjects/cms_blog/static/' + vlog.filename
    db.session.delete(vlog)
    db.session.commit()
    os.remove(remove_file)
    return redirect(url_for('admin.manage_vlog'))