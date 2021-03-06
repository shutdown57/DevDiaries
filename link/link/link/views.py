from flask import render_template, request, flash, redirect, url_for
from urllib.parse import urlparse
from flask_login import current_user, login_required

from link import bp_link
from link import utils as fetch
from common.extensions import db
from link.models import Link, Tag


@bp_link.route('/', methods=['GET'])
def index():
    per_page = 10
    page = request.args.get('page', 1, type=int)
    links = Link.query.order_by(
        Link.created_at.desc()
    ).paginate(page, per_page=per_page, error_out=False)
    return render_template('link/index.html', links=links)


@bp_link.route('/create', methods=['GET'])
@login_required
def create():
    return render_template('link/create.html')


@bp_link.route('/store', methods=['POST'])
@login_required
def store():
    data = request.form.copy()
    if all(['name', 'url', 'tags', 'description']) not in data.keys():
        link = Link.query.filter_by(url=data['url']).first()
        if not link:
            url_info = urlparse(data['url'])
            link = Link(
                user_id=current_user.id,
                url=data['url'],
                description=data['description'],
                name=data['name'])
            for tag_name in data['tags'].split(','):
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
            fetch.make_img(data['url'], str(link.id))
            return redirect(url_for('bp_link.show', id=link.id))
        flash("Data exist", "error")
        return redirect(url_for('bp_link.show', id=link.id))
    flash("fill require inputs", "error")
    return redirect(url_for('bp_link.create'))


@bp_link.route('/p2i_callback', methods=['GET', 'POST'])
def call_back():
    if 'status' in request.form and request.form['status'] == 'finished':
        link_id = request.args.get('link_id', '')
        if not link_id:
            return '', 200
        link = Link.query.filter_by(id=link_id).first()
        link.website_image = fetch.write_img(request.form['image_url'])
        db.session.add(link)
        db.session.commit()
    return '', 200


@bp_link.route('/<int:id>', methods=['GET'])
def show(id):
    link = Link.query.filter_by(id=id).first()
    if not link:
        flash("Link does not exist", "error")
        return redirect('bp_link.index')
    #  if not link.has_image:
        #  link.p2i_address = fetch.make_img(link.url, str(link.id))
        #  link.has_image = True
        #  fetch.write_img(link.p2i_address)
        #  db.session.add(link)
        #  db.session.commit()
    return render_template('/link/show.html', link=link)
