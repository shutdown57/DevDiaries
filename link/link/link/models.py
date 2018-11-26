from common.extensions import db
from common.utils import timestamp


link_tag_table = db.Table(
    'link_tag',
    db.Column('link_id', db.Integer, db.ForeignKey('link.id'), nullable=False),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), nullable=False)
)


class Link(db.Model):
    """
    Link model
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

    name = db.Column(db.String(256), nullable=False, unique=True)
    url = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, default=True)
    website_image = db.Column(db.String(256))
    description = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    tags = db.relationship('Tag',
                           secondary=link_tag_table,
                           backref=db.backref('links', lazy='dynamic'))

    def to_json(self):
        """
        Convert link object to dict (json like)
        :return: dict
        """
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
        """
        Represent link object
        :return: str
        """
        return '<LINK ID={id} URL={url} ACTIVE={active}>'.format(
            id=self.id, url=self.url, active=self.active)

    @classmethod
    def create(cls, name, url, description):
        """
        Create link object and store in database
        :param cls Link: Class inctanse
        :param name str: website name
        :param url str: website url
        :param description str: describe website
        :return: Link object
        """
        link = cls(name=name, url=url, description=description)
        db.session.add(link)
        db.session.commit()
        return link


class Tag(db.Model):
    """
    Tag model
    Fields: id <int>,
            created_at <int>,
            updated_at <int>,
            name <str>
    Input fields: name <str>
    """
    __tablename__ = 'tag'
    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.Integer, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp)

    name = db.Column(db.String(50), nullable=False)

    @classmethod
    def create(cls, name):
        """
        Create Tag object and store in database
        :param cls Tag: Class inctanse
        :param name str: Name of tag
        :return: Tag object
        """
        tag = cls(name=name)
        db.session.add(tag)
        db.session.commit()
        return tag

    def to_json(self):
        """
        Convert tag object to dict (json like)
        :return: dict
        """
        return {
            'ID': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        """
        Represent tag object
        :return: str
        """
        return '<TAG ID={id} NAME={name}>'.format(
            id=self.id, name=self.name)
