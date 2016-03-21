"""Models needed for Article module"""

from flask import flash

from acm_phoenix.extensions import db
from acm_phoenix.users.models import User
from acm_phoenix.users.gfm import gfm

import re
from datetime import datetime

slug_re = re.compile('[a-zA-Z0-9]+')
def slugify(title):
    """
    Change title into shortened slug to be used in urls.
    """
    _title = title[:99].replace(' ', '-')  # Changed slug length to 100
    return '-'.join(re.findall(slug_re, _title))

class Category(db.Model):
    """
    A Category for a Post
    """
    __tablename__ = 'articles_category'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    slug = db.Column(db.Text)

    def __init__(self, title='', slug=None):
        self.title = title
        self.slug = slugify(title)

    def __unicode__(self):
        return self.title

# M2M Relationship between tags and posts
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('articles_tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('articles_posts.id'))
)

class Tag(db.Model):
    """
    A post tag.
    """
    __tablename__ = 'articles_tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    def __init__(self, tagname=''):
        self.name = tagname

    def __unicode__(self):
        return self.name

class Post(db.Model):
    """
    A Post or article with a category, tags, and an author.
    Stored content is github flavored markdown'd.
    """
    __tablename__ = 'articles_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    gfm_content = db.Column(db.Text)
    created = db.Column(db.DateTime)
    tags = db.relationship('Tag', secondary=tags,
                           primaryjoin=(id == tags.c.post_id),
                           secondaryjoin=(Tag.id == tags.c.tag_id),
                           backref=db.backref('tags', lazy='dynamic'))
    slug = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('articles_category.id'))
    category = db.relationship('Category', 
                               primaryjoin=(category_id == Category.id),
                               backref=db.backref('cats', lazy='dynamic'),
                               order_by=Category.slug)
    author_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))
    author = db.relationship('User', primaryjoin=(author_id == User.id),
                             backref=db.backref('posters', lazy='dynamic'),
                             order_by=User.name)

    def __init__(self, title='', gfm_content='', created=None, tags=[],
                 slug=None, category=None, author=None):
        self.title = title
        self.gfm_content = gfm(gfm_content)
        self.created = created or datetime.now()
        self.tags = tags
        self.slug = slugify(title)
        self.category = category
        self.author = author

    def __unicode__(self):
        return self.slug
