from common.extensions import db
from common.utils import timestamp


link_tag_table = db.Table(
    'link_tag',
    db.Column('link_id', db.Integer, db.ForeignKey('link.id'), nullable=False),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), nullable=False)
)


class Link(db.Model):
    """Link model
    Fields: id <int>,
            created_at <int>,
            updated_at <int>,
            name <str>,
            url <str>,
            active <bool>,
            website_image <str>,
            description <str>,
            user_id <int>,
            tags <Tag>
    Input fields: name, url, description
    """
    __tablename__ = 'link'
    __searchable__ = ['name', 'url', 'description']

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.Integer, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp)

    name = db.Column(db.String, nullable=False, unique=True)
    url = db.Column(db.Text, nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)
    website_image = db.Column(db.String)
    description = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    tags = db.relationship('Tag',
                           secondary=link_tag_table,
                           backref=db.backref('links', lazy='dynamic'))

    # TODO make a function to create link object
    def to_json(self):
        return {
            'ID': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'url': self.url,
            'active': self.active,
            'name': self.name,
            'image': self.website_image,
            'description': self.description,
            'tags': [tag.to_json() for tag in self.tags]
        }

    def __repr__(self):
        return '<LINK ID={id} URL={url} ACTIVE={active}>'.format(
            id=self.id, url=self.url, active=self.active
        )


class Tag(db.Model):
    """
    Fields: id <int>,
            created_at <int>,
            updated_at <int>,
            name <str>
    Input fields: name <str>"""
    __tablename__ = 'tag'
    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.Integer, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp)

    name = db.Column(db.String, nullable=False)

    def to_json(self):
        return {
            'ID': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return '<TAG ID={id} NAME={name}>'.format(
            id=self.id, name=self.name)
