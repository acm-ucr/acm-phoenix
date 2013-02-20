"""Tests for model creation and editing in the articles module."""

from tests import ACMTestCase
from acm_phoenix import db
from acm_phoenix.users.models import User
from acm_phoenix.articles.models import Category, Tag, Post, slug_re, slugify

from acm_phoenix.users.gfm import gfm
from datetime import datetime

class CategoryModelTest(ACMTestCase):
    """Unit tests for the Category SQL Model."""

    # Helper functions for testing interactions
    def remove_cat(self, cat):
        """Removes a specific category from the database."""
        db.session.delete(cat)
        db.session.commit()

    def add_cat(self, cat = None):
        """Adds a category to the database.

        cat is optional, so if no cat is passed in, the default Category object
        will be used instead."""
        if cat is None:
            cat = Category()
        db.session.add(cat)
        db.session.commit()

    def test_no_default_categories(self):
        """Tests that there are no default categories in the database."""
        cat = Category.query.first()
        self.assertIsNone(cat)

    def test_add_category_to_db(self):
        """Tests that categories can be added to database."""
        cat = Category()
        self.add_cat(cat)

        self.assertIn(cat, db.session)
        self.remove_cat(cat)

    def test_remove_category_from_db(self):
        """Tests that categories can be removed from the database."""
        self.add_cat()

        cat = Category.query.first()
        self.remove_cat(cat)
        self.assertNotIn(cat, db.session)

    def test_default_cat_values(self):
        """Tests that the value for a default Category are as expected."""
        self.add_cat()
        cat = Category.query.first()
        self.assertEquals(cat.title, "")
        self.assertEquals(cat.slug, "")

        self.remove_cat(cat)

    def test_modify_cat_from_db(self):
        """Tests that a Category Object can be modified and recommited."""
        self.add_cat()
        cat = Category.query.first()

        cat.title = "Test Category"
        cat.slug = slugify(cat.title)

        self.add_cat(cat)
        cat = Category.query.first()

        self.assertEquals(cat.title, "Test Category")
        self.assertEquals(cat.slug, slugify(cat.title))

        self.remove_cat(cat)

    def test_create_cat_with_ctor(self):
        """Tests the constructor for the Category Model."""
        cat = Category("Test Category")
        self.add_cat(cat)

        cat = Category.query.first()

        self.assertEquals(cat.title, "Test Category")
        self.assertEquals(cat.slug, slugify(cat.title))
        self.remove_cat(cat)

    def test_cat_slugify(self):
        """Tests that slugification works as expected."""
        cat = Category("Test Category")
        self.assertEquals(cat.slug, slugify(cat.title))

    def test_unicode_repr(self):
        """Tests that __unicode__ representation is as expected."""
        cat = Category("Test Category")
        self.assertEquals(cat.__unicode__(), "Test Category")

class TagModelTest(ACMTestCase):
    """Unit tests for the Tag SQL Model."""

    # Helper functions for testing interactions
    def remove_tag(self, tag):
        """Removes a specific tag from the database."""
        db.session.delete(tag)
        db.session.commit()

    def add_tag(self, tag = None):
        """Adds a tag to the database.

        tag is optional, so if no tag is passed in, the default Tag object
        will be used instead."""
        if tag is None:
            tag = Tag()
        db.session.add(tag)
        db.session.commit()

    def test_no_default_tags(self):
        """Tests that there are no default tags in the database."""
        tag = Tag.query.first()
        self.assertIsNone(tag)

    def test_add_tag_to_db(self):
        """Tests that tags can be added to database."""
        tag = Tag()
        self.add_tag(tag)

        self.assertIn(tag, db.session)
        self.remove_tag(tag)

    def test_remove_tag_from_db(self):
        """Tests that tags can be removed from the database."""
        self.add_tag()

        tag = Tag.query.first()
        self.remove_tag(tag)
        self.assertNotIn(tag, db.session)

    def test_default_tag_values(self):
        """Tests that the value for a default Tag are as expected."""
        self.add_tag()
        tag = Tag.query.first()
        self.assertEquals(tag.name, '')

        self.remove_tag(tag)

    def test_modify_tag_from_db(self):
        """Tests that a Tag Object can be modified and recommited."""
        self.add_tag()
        tag = Tag.query.first()

        tag.name = "Test Tag"

        self.add_tag(tag)
        cat = Category.query.first()

        self.assertEquals(tag.name, "Test Tag")

        self.remove_tag(tag)

    def test_create_tag_with_ctor(self):
        """Tests the constructor for the Tag Model."""
        tag = Tag("Test Tag")
        self.add_tag(tag)

        tag = Tag.query.first()

        self.assertEquals(tag.name, "Test Tag")
        self.remove_tag(tag)

    def test_unicode_repr(self):
        """Tests that __unicode__ representation is as expected."""
        tag = Tag("Test Tag")
        self.assertEquals(tag.__unicode__(), "Test Tag")

class PostModelTest(ACMTestCase):
    """Unit tests for the Post SQL Model."""

    # Helper functions for testing interactions
    def remove_post(self, post):
        """Removes a specific post from the database."""
        db.session.delete(post)
        db.session.commit()

    def add_post(self, post = None):
        """Adds a post to the database.

        post is optional, so if no post is passed in, the default Post object
        will be used instead."""
        if post is None:
            post = Post()
        db.session.add(post)
        db.session.commit()

    def test_no_default_posts(self):
        """Tests that there are no default tags in the database."""
        post = Post.query.first()
        self.assertIsNone(post)

    def test_add_post_to_db(self):
        """Tests that posts can be added to database."""
        post = Post()
        self.add_post(post)

        self.assertIn(post, db.session)
        self.remove_post(post)

    def test_remove_post_from_db(self):
        """Tests that posts can be removed from the database."""
        self.add_post()

        post = Post.query.first()
        self.remove_post(post)
        self.assertNotIn(post, db.session)

    def test_default_post_values(self):
        """Tests that the values for a default Post are as expected."""
        now = datetime.now()

        self.add_post()
        post = Post.query.first()
        later = datetime.now()

        self.assertEquals(post.title, '')
        self.assertEquals(post.gfm_content, gfm(''))
        self.assertEquals(post.slug, slugify(post.title))
        self.assertIsNone(post.author)
        self.assertIsNone(post.category)
        self.assertEquals(post.tags, [])
        self.assertGreaterEqual(post.created, now)
        self.assertLessEqual(post.created, later)
        self.remove_post(post)

    def test_modify_post_from_db(self):
        """Tests that a Post Object can be modified and recommited."""
        self.add_post()
        post = Post.query.first()

        now = datetime.now()
        post.title = "Test Post"
        post.gfm_content = gfm("Test Content")
        post.created = now
        post.slug = slugify(post.title)

        tag = Tag("Test Tag")
        post.tags = [tag]
        
        cat = Category("Test Category")
        post.category = cat

        user = User("Test User")
        post.author = user

        self.add_post(post)
        post = Post.query.first()

        self.assertEquals(post.title, "Test Post")
        self.assertEquals(post.gfm_content, gfm("Test Content"))
        self.assertEquals(post.created, now)
        self.assertEquals(post.tags, [tag])
        self.assertEquals(post.slug, slugify(post.title))
        self.assertEquals(post.category, cat)
        self.assertEquals(post.author, user)

        self.remove_post(post)

    def test_create_post_with_ctor(self):
        """Tests the constructor for the Post Model."""
        now = datetime.now()
        tag = Tag("Test Tag")
        category = Category("Test Category")
        user = User("Test User")
        post = Post("Test Post", "## Test H2", now, [tag], None,
                    category, user)
        self.add_post(post)

        post = Post.query.first()

        self.assertEquals(post.title, "Test Post")
        self.assertEquals(post.gfm_content, gfm("## Test H2"))
        self.assertEquals(post.created, now)
        self.assertEquals(post.tags, [tag])
        self.assertEquals(post.slug, slugify(post.title))
        self.assertEquals(post.category, category)
        self.assertEquals(post.author, user)

        self.remove_post(post)

    def test_unicode_repr(self):
        """Tests that Post.__unicode__ representation is as expected."""
        post = Post("Test Post")
        self.assertEquals(post.__unicode__(), slugify(post.title))

    def test_post_relationships(self):
        """Tests that Post database relationships work as expected."""

        # Set up referenced database data
        tags = [Tag("Test Tag1"), Tag("Test Tag2"), Tag("Test Tag3")]
        category = Category("Test Category")
        author = User("Test Author")

        for tag in tags:
            db.session.add(tag)
        db.session.add(category)
        db.session.add(author)
        db.session.commit()

        post = Post("Test Post", "Test content", None, tags, None, category,
                    author)
        self.add_post(post)

        post = Post.query.first()

        author_query = User.query.get(post.author_id)
        self.assertEqual(author, author_query)
        cat_query = Category.query.get(post.category_id)
        self.assertEqual(category, cat_query)
        self.assertItemsEqual(post.tags, tags)

        for tag in tags:
            db.session.delete(tag)
        db.session.delete(category)
        db.session.delete(author)
        self.remove_post(post)
