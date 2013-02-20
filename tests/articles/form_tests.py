"""Tests for form creation and editing."""

from tests import ACMFormTest
from acm_phoenix.users.models import User
from acm_phoenix.articles.models import Post, Category, Tag
from acm_phoenix.articles.forms import (all_cats, all_publishers, all_tags,
                                        SearchForm)
from flask.ext.wtf import (TextField, SelectField, QuerySelectMultipleField)

class ArticlesFormsTest(ACMFormTest):
    """Unit tests for Articles Forms."""
    __test__ = True
    forms = [SearchForm]

    def test_necessary_fields_in_form(self):
        """Tests that necessary fields are in forms to be tested."""
        query_fields = ['query', 'category', 'author', 'tags', 'order_by']

        form = SearchForm()
        self.assertTrue(self.fields_in_form(form, query_fields))

    def test_fields_have_expected_types(self):
        """Tests that each field has expected Field type."""
        form = SearchForm()
        self.assertType(form, 'query', TextField)
        self.assertType(form, 'category', QuerySelectMultipleField)
        self.assertType(form, 'author', QuerySelectMultipleField)
        self.assertType(form, 'tags', QuerySelectMultipleField)
        self.assertType(form, 'order_by', SelectField)

    def test_select_fields_have_expected_choices(self):
        """Tests that each SelectField in the form has the expected choices."""
        order_by_choices = [('created%20DESC', 'Recency'),
                            ('title', 'Title'),
                            ('articles_category.slug', 'Category Name'),
                            ('users_user.name', 'Author Name')]

        form = SearchForm()
        self.assertChoices(form, 'order_by', order_by_choices)
        self.assertChoiceValues(form, 'order_by', order_by_choices)

    def test_fields_have_expected_validators(self):
        """Tests that form fields have the expected validators."""
        form = SearchForm()
        self.assertOptional(form, 'query')
        self.assertOptional(form, 'category')
        self.assertOptional(form, 'author')
        self.assertOptional(form, 'tags')
        self.assertRequired(form, 'order_by')

    def test_required_fields_make_form_valid(self):
        """Tests that form is valid iff required fields are valid."""
        form = SearchForm(order_by='title')
        self.assertTrue(form.validate())

        # Testing that form with optional fields filled out is valid.
        cat = Category('Test Cat')
        author = User('Test Author')
        tag = Tag('Test Tag')
        form = SearchForm(query='Test Query', category=[cat], author=[author],
                          tags=[tag], order_by='title')
        self.assertTrue(form.validate())

    def test_forms_populate_models(self):
        """Search form doesn't modify a model."""
        pass
