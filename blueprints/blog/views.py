from flask import Blueprint, render_template, url_for, redirect, request
from blueprints.models import PostSeven, PostCc, Post_life, Post_journal,CategoryCc, \
     Photo,Album
import re

blog_bp = Blueprint('blog',__name__)

'''
***************
过滤器
***************
'''
@blog_bp.app_template_filter('display_post')
def desplay_post(body):
    pattern = re.compile('<p>[^<].*?</p>')
    return ''.join(pattern.findall(body))

@blog_bp.app_template_filter('display_img')
def dis_play_img(body):
    pattern = re.compile('/admin/uploads/(.*?)/')
    return pattern.findall(body)

'''
***************
首页
***************
'''
@blog_bp.route('/', methods=['GET'])
def home():
    return render_template('blog/home.html')


'''
***************
77的博客
***************
'''
@blog_bp.route('/77_blog/', methods=['GET'])
def seven_blog():
    page = request.args.get('page', 1, type=int)
    pagination = PostSeven.query.order_by(PostSeven.timestamp.desc()).paginate(
        page, per_page=15, error_out=False)
    posts = pagination.items
    return render_template("blog/77's_Blog.html",pagination=pagination, posts=posts)


'''
***************
CC的博客
***************
'''
@blog_bp.route('/CC_blog/', methods=['GET'])
def cc_blog():
    page = request.args.get('page', 1, type=int)
    pagination = PostCc.query.order_by(PostCc.timestamp.desc()).paginate(
        page, per_page=15, error_out=False)
    posts = pagination.items
    pagination_category = CategoryCc.query.paginate(
        1, per_page=CategoryCc.query.count())
    categorys = pagination_category.items
    return render_template("blog/CC's_Blog.html",pagination=pagination, posts=posts, categorys=categorys)

@blog_bp.route('/CC_blog/category/<int:category_id>/', methods=['GET'])
def  cc_category_blog(category_id):
    page = request.args.get('page', 1, type=int)
    pagination = PostCc.query.filter_by(category_cc_id=category_id).order_by(
        PostCc.timestamp.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items
    pagination_category = CategoryCc.query.paginate(
        1, per_page=CategoryCc.query.count())
    categorys = pagination_category.items
    return render_template("blog/CC's_Blog_Category.html", pagination=pagination, posts=posts, categorys=categorys)

@blog_bp.route('/CC_blog/post/<int:post_id>/', methods=['GET'])
def cc_post_blog(post_id):
    post = PostCc.query.get_or_404(post_id)
    pagination_category = CategoryCc.query.paginate(
        1, per_page=CategoryCc.query.count())
    categorys = pagination_category.items
    return render_template("blog/CC's_Blog_detail.html", post=post, categorys=categorys)


'''
***************
Love
***************
'''
@blog_bp.route('/Love/', methods=['GET'])
def love():
    return  render_template('blog/love.html')


'''
***************
Life
***************
'''
@blog_bp.route('/Life/', methods=['GET'])
def life():
    page = request.args.get('page', 1, type=int)
    pagination = Post_life.query.order_by(Post_life.timestamp.desc()).paginate(
        page, per_page=15, error_out=False)
    posts = pagination.items
    return render_template("blog/Life.html", pagination=pagination, posts=posts)

'''
***************
Album
***************
'''
@blog_bp.route('/Album/', methods=['GET'])
def album():
    pagination = Album.query.order_by(Album.timestamp.desc()).paginate(
        1, per_page=Album.query.count(), error_out=False)
    albums = pagination.items
    return render_template('blog/Album.html', albums=albums)

@blog_bp.route('/Album/<int:album_id>/', methods=['GET'])
def photo(album_id):
    page = request.args.get('page', 1, type=int)
    pagination = Photo.query.filter_by(album_id=album_id).order_by(Photo.timestamp.desc()).paginate(
        page, per_page=Photo.query.filter_by(album_id=album_id).count(), error_out=False)
    photos = pagination.items
    return render_template('blog/Photo.html', pagination=pagination, photos=photos)