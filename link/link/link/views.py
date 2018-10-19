from flask import render_template
from urllib.parse import urlparse
from flask import request

from common.extensions import db
from common.utils import response
from link import bp_link
from auth.auth import token_auth
from link.models import Link, Tag


@bp_link.route('/', methods=['GET'])
def index(pages=None):
    links = Link.query.paginate()
    return render_template('link/index.html', links=links)


@bp_link.route('/pages/<int:page>', methods=['GET'])
@bp_link.route('/', methods=['GET'])
def get_links(page: int=None):
    links = Link.query.paginate()
    if not page:
        data = {
            'has_prev': links.has_prev,
            'has_next': links.has_next,
            'pages': links.pages,
            'links': [link.to_json() for link in links.items],
            'page': links.page,
            'total': links.total
        }
        return response(data=data)
    elif links.pages >= page:
        links.page = page
        data = {
            'has_prev': links.has_prev,
            'has_next': links.has_next,
            'pages': links.pages,
            'links': [link.to_json() for link in links.items],
            'page': links.page,
            'total': links.total
        }
        return response(data=data)
    else:
        return response(status_code=404)


@bp_link.route('/<int:id>', methods=['GET'])
def get_link(id: int):
    link = Link.query.filter_by(id=id).first()
    if link:
        return response(data=link.to_json(), status_code=200)
    return response(status_code=404)


@bp_link.route('/', methods=['POST'])
@token_auth.login_required
def create_link():
    data = request.get_json()
    if data and 'url' in data and 'description' in data and 'tags' in data and data['tags']:
        link = Link.query.filter_by(url=data['url']).first()
        if not link:
            url_info = urlparse(data['url'])
            link = Link(url=data['url'], description=data['description'], name=url_info.netloc)
            for tag_name in data['tags']:
                old_tag = Tag.query.filter_by(name=tag_name).first()
                if old_tag:
                    link.tags.append(old_tag)
                    db.session.add(link)
                    continue
                tag = Tag(name=tag_name)
                db.session.add(tag)
                link.tags.append(tag)
                db.session.add(link)
            db.session.commit()
            return response(data=link.to_json(), status_code=201)
        return response(status_code=409)
    return response(status_code=400)


@bp_link.route('/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_link(id: int):
    link = Link.query.filter_by(id=id).first()
    if not link:
        return response(status_code=404)
    data = request.get_json()
    if data:
        for key in data:
            if hasattr(link, key):
                setattr(link, key, data[key])
                db.session.add(link)
        db.session.commit()
        return response(data=link.to_json(), status_code=201)
    return response(status_code=400)


@bp_link.route('/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_link(id: int):
    link = Link.query.filter_by(id=id).first()
    if not link:
        return response(status_code=404)
    url = link.url
    db.session.delete(link)
    db.session.commit()
    return response(message='Link {url} has been deleted'.format(url=url),
                    status_code=202)


@bp_link.route('/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.get().all()
    if tags:
        tags = [tag.to_json() for tag in tags]
        return response(data=tags, status_code=200)
    return response(status_code=404)


@bp_link.route('/tags/<int:id>', methods=['GET'])
@token_auth.login_required
def update_tag(id: int):
    tag = Tag.query.filter_by(id=id).first()
    if not tag:
        return response(status_code=404)
    data = request.get_json()
    if data and 'name' in data:
        tag.name = data['name']
        db.session.add(tag)
        db.session.commit()
        return response(data=tag.to_json(), status_code=202)
    return response(status_code=400)


@bp_link.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    if data:
        pass
    return response(status_code=404)
