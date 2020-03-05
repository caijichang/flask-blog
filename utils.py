try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for, current_app
import uuid
import os
from PIL import Image


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
       # print('target=', target)
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def allowed_file_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['BLOG_ALLOWED_IMAGE_EXTENSIONS']

def allowed_file_movie(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['BLOG_ALLOWED_MOVIE_EXTENSIONS']

def  random_filename_uuid(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename

#判断文件夹是否存在
def confirm_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def resize_image(image, filename):
    filename, ext = os.path.splitext(filename)
    img = Image.open(image)
    if (img.size[0] / img.size[1] < 1.3):
        cropped = img.crop((0, 200, 960, 920))
    else:
        cropped = img.crop((0, 0, img.size[0], img.size[0]/1.3333333333333333333))
    base_path = '/Users/caijichang/PycharmProjects/cms_blog/static'
    path = os.path.join(base_path, filename)
    path = path + '_small' + ext
    cropped.save(path, optimize=True, quality=85)
    filename = filename + '_small' + ext
    return filename


