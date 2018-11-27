import os
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor
from flask import render_template, request, flash, redirect, url_for
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required

from common.extensions import db
from common.utils import allowed_file
from link import bp_link
from config import Config
from link.models import Link, Tag


executor = ThreadPoolExecutor(max_workers=1)


@bp_link.route('/', methods=['GET'])
def index(pages=None):
    links = Link.query.paginate()
    return render_template('link/index.html', links=links)


@bp_link.route('/create', methods=['GET'])
@login_required
def create():
    return render_template('link/create.html')


@bp_link.route('/store', methods=['POST'])
@login_required
def store():
    data = request.form.copy()
    # TODO better validation
    if data and 'url' in data.keys() and 'description' in data.keys() and \
            'tags' in data.keys() and data['tags']:
        link = Link.query.filter_by(url=data['url']).first()
        if not link:
            # resp = make_img(data['url'], data['name'], )
            #  img_url = get_img(resp['image_url'], data['name'])
            url_info = urlparse(data['url'])
            link = Link(
                user_id=current_user.id,
                url=data['url'],
                description=data['description'],
                name=url_info.netloc)
            for tag_name in data['tags'].split(','):
                old_tag = Tag.query.filter_by(name=tag_name).first()
                if old_tag:
                    link.tags.append(old_tag)
                    db.session.add(link)
                    continue
                tag = Tag(name=tag_name)
                db.session.add(tag)
                link.tags.append(tag)
            executor.submit(make_img, data['url'], url_info.netloc, link.id)
            db.session.add(link)
            db.session.commit()
            return redirect(url_for('bp_link.show', id=link.id))
        flash("Data exist", "error")
        return redirect(url_for('bp_link.show', id=link.id))
    flash("fill require inputs", "error")
    return redirect(url_for('bp_link.create'))


@bp_link.route('/p2i_callback', methods=['POST'])
def call_back():
    print("They call me!", request.form)
    return '', 200


def make_img(p2i_url: str, name: str, link_id: int) -> None:
    """
    Make image screenshut
    :param p2i_url str: Website url to make screenshut
    :param name str: Website name
    :param link_id int: Link id object to store image url
    """
    p2i = {
        'p2i_url': p2i_url,
        'p2i_key': os.environ.get('P2I_KEY', ''),
        'p2i_device': 6,
        'p2i_fullpage': 1,
        'p2i_imageformat': 'jpg',
        'p2i_size': '600x0',
        'p2i_callback': 'http://localhost:5000/links/call_back',
        'p2i_screen': '1024x768'
    }

    request_url = 'http://api.page2images.com/restfullink'
    data = request_img(request_url, p2i)
    time.sleep(3000)
    data = request_img(request_url, p2i)

    # double check to sure image screenshut is done
    if data.json()['status'] == 'processing':
        time.sleep(3000)
        data = request_img(request_url, p2i)

    img_url = write_image(data.json()['image_url'], name)
    if img_url:
        link = Link.query.filter_by(id=link_id).first()
        link.website_image = img_url
        db.session.add(link)
        db.session.commit()
    #  print(data.json()['status'])
    # "status":"processing"
    # "status":"finished","image_url":"http://api.page2images.com/ccimages/ea/e9/0F0RnDufDEfr5pVS.jpg"


def request_img(request_url: str, param: dict) -> dict:
    """
    Get request to p2i api to make screenshut
    :param request_url str: Website we want to make screenshut
    :param param dict: Configuration to make screenshut
    :return: Response of p2i api
    """
    try:
        data = requests.get(request_url, params=p2i)
    except Exception as e:
        print(f"Error in [get image url]: {e}")
        raise # TODO enter exception class
    return data


def write_img(img_url, img_name):
    """
    Download and write image to disk
    :param img_url str: The image url of screenshut
    :param img_name str: Name of file
    """
    img_name = '-'.join(img_name.split('/')[-1])
    #  img_url = 'http://api.page2images.com/ccimages/cf/77/tE2byaNynW4mGgQ2.jpg'
    if not img_url:
        print("Image url required")
        raise # TODO enter exception class
    try:
        img_file = requests.get(img_url).content
    except Exception as e:
        print(f"Error in [get image url]: {e}")
        raise # TODO enter exception class
    if img_file and allowed_file(img_name):
        img_name = secure_filename(img_name)
        with open(Config.UPLOAD_FOLDER + '/' + img_name, 'wb') as image:
            image.write(img_file)
        return Config.UPLOAD_FOLDER + '/' + img_name


@bp_link.route('/<int:id>', methods=['GET'])
def show(id):
    link = Link.query.filter_by(id=id).first()
    if not link:
        flash("Link does not exist", "error")
        return redirect('bp_link.index')
    return render_template('/link/show.html', link=link)
