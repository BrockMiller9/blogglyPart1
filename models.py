"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


# TODO Create user modal

class User(db.Model):

    """Displays the users table"""
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(db.String(1000))

    def __repr__(self):
        """Show info about user."""

        p = self
        return f"<User {p.id} {p.first_name} {p.last_name} {p.image_url}>"


class Post(db.Model):

    """One user can have many posts. Shares a foreign key with User"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.Date, default='2023-03-16')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='posts')

    tag = db.relationship('Tag', secondary='post_tags',
                          backref='posts', lazy='dynamic')

    def __repr__(self):
        """Show info about user."""

        p = self
        return f"<User {p.id} {p.title} {p.content} {p.user_id}>"


class Tag(db.Model):

    """Tag class"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text, nullable=False)

    project = db.relationship('Post', secondary='post_tags', backref='tags')

    def __repr__(self):
        """Show info about user."""

        p = self
        return f"<Tag {p.id} {p.name}>"


class PostTag(db.Model):
    """Each Post can have multiple tags"""
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey(
        'tags.id'), primary_key=True)
