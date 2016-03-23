"""Forms that will be used with the Articles models"""
                           
from flask_wtf import Form
from wtforms import TextField, SelectField
from wtforms.validators import Optional, Required
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

from acm_phoenix.users.models import User
from acm_phoenix.articles.models import Category, Tag

def all_cats():
    """
    Get all categories in alphabetical order.
    """
    return Category.query.order_by('title').all()

def all_publishers():
    """
    Get all users with at least a publisher role.
    """
    return User.query.filter(User.role <= 1).order_by('name').all()

def all_tags():
    """
    Get all tags in alphabetical order.
    """
    return Tag.query.order_by('name').all()

class SearchForm(Form):
    """
    Form used to help Users find articles.
    """
    query = TextField(u'Search Query', [Optional()])
    category = QuerySelectMultipleField(u'In Category', [Optional()],
                                        query_factory=all_cats)
    author = QuerySelectMultipleField(u'Authored By', [Optional()],
                                      query_factory=all_publishers)
    tags = QuerySelectMultipleField(u'With Tags', [Optional()],
                                    query_factory=all_tags)

    order_by = SelectField(u'Order by', [Required()], default='created',
                           choices=[('created%20DESC', 'Recency'),
                                    ('title', 'Title'),
                                    ('articles_category.slug', 'Category Name'),
                                    ('users.name', 'Author Name')]
                           )
