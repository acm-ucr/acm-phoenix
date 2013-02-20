"""Tests for form creation and editing."""

from tests import ACMFormTest
from acm_phoenix.extensions import db
from acm_phoenix.users.models import User
from acm_phoenix.users import constants as USER
from acm_phoenix.articles.models import Post, Category, Tag
from acm_phoenix.articles.forms import (all_cats, all_publishers, all_tags,
                                        SearchForm)
from flask.ext.wtf import (TextField, SelectField, QuerySelectMultipleField)

class ArticlesFormsTest(ACMFormTest):
    """Unit tests for Articles Forms."""
    __test__ = True
    forms = [SearchForm]

    def test_all_cats(self):
        """Tests that all_cats() gives all categories in alphabetical order."""
        cats = all_cats()
        self.assertEquals(cats, [])

        cats = [Category("Test Cat 1"), Category("Test Cat 3"),
                Category("Test Cat 0")]
        for cat in cats:
            db.session.add(cat)
        db.session.commit()

        result_cats = all_cats()
        self.assertNotEqual(result_cats, [])
        cats.sort(key=lambda cat: cat.title)
        self.assertEquals(len(result_cats), 3)
        self.assertEquals(cats, result_cats)

        for cat in cats:
            db.session.delete(cat)
        db.session.commit()

    def test_all_publishers(self):
        """Tests that all_publishers gives all authors in alphabetical order."""
        authors = all_publishers()
        self.assertEqual(authors, [])

        users = [User("Test User 0"), User("Test User 1"),
                 User("Test Author 5"), User("Test Author 1")]
        for user in users:
            db.session.add(user)
        db.session.commit()
        authors = users[2:]

        # Should still be an empty list since none of the users are authors.
        result_authors = all_publishers()
        self.assertEquals(result_authors, [])

        authors[0].role = USER.PUBLISHER
        authors[1].role = USER.ADMIN
        for author in authors:
            db.session.add(author)
        db.session.commit()

        # Should finally have the admin and publisher
        result_authors = all_publishers()
        self.assertNotEqual(result_authors, [])
        self.assertEquals(len(result_authors), 2)
        authors.sort(key=lambda user: user.name)
        self.assertEquals(authors, result_authors)

        for user in users:
            db.session.delete(user)
        db.session.commit()

    def test_all_tags(self):
        """Tests that all_tags() gives all tags in alphabetical order."""
        tags = all_tags()
        self.assertEqual(tags, [])

        tags = [Tag("Test tag 3"), Tag("Test tag 0")]
        for tag in tags:
            db.session.add(tag)
        db.session.commit()

        result_tags = all_tags()
        self.assertNotEqual(result_tags, [])
        self.assertEquals(len(result_tags), 2)
        tags.sort(key=lambda tag: tag.name)
        self.assertEquals(tags, result_tags)

        for tag in tags:
            db.session.delete(tag)
        db.session.commit()

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
