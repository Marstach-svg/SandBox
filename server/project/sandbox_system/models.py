from datetime import datetime
from pytz import timezone
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

from sandbox_system import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    introduce = db.Column(db.Text)
    tech = db.Column(db.Text)
    job = db.Column(db.String(64))
    image = db.Column(db.String(140))
    password_hash = db.Column(db.String(128))
    administrator = db.Column(db.String(1))
    blog = db.relationship('Blog', backref = 'author', lazy = 'dynamic')
    blog_comment = db.relationship('BlogComment', backref='commenter', lazy='dynamic')
    chat_message = db.relationship('ChatMessage', backref='chat_user', lazy='dynamic')

    def __init__(self, email, username, introduce, tech, job, image, password, administrator):
        self.email = email
        self.username = username
        self.introduce = introduce
        self.tech = tech
        self.job = job
        self.image = image
        self.password = password
        self.administrator = administrator

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_administrator(self):
        if self.administrator == '1':
            return 1
        else:
            return 0


class Blog(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime, default=datetime.now(timezone('Asia/Tokyo')))
    category_id = db.Column(db.Integer, db.ForeignKey('blog_category.id'))
    title = db.Column(db.String(140))
    text = db.Column(db.Text)
    summary = db.Column(db.String(140))
    image = db.Column(db.String(140))

    def __init__(self, title, text, summary, image, user_id, category_id):
        self.title = title
        self.text = text
        self.summary = summary
        self.user_id = user_id
        self.image = image
        self.category_id = category_id


class OtherBlog(db.Model):
    __tablename__ = 'otherblog'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    summary = db.Column(db.String(140))
    category_id = db.Column(db.Integer, db.ForeignKey('blog_category.id'))
    text = db.Column(db.Text)
    url = db.Column(db.String(140))
    image = db.Column(db.String(140))

    def __init__(self, title, summary, url, text, image, category_id):
        self.title = title
        self.summary = summary
        self.url = url
        self.text = text
        self.image = image
        self.category_id = category_id


class BlogFavorite(db.Model):
    __tablename__ = 'blog_favorite'

    id = db.Column(db.Integer, primary_key=True)
    favorite_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('blog_category.id'))
    title = db.Column(db.String(140))
    text = db.Column(db.Text)
    summary = db.Column(db.String(140))
    image = db.Column(db.String(140))

    def __init__(self, title, text, summary, image, favorite_user_id, blog_id, category_id):
        self.title = title
        self.text = text
        self.summary = summary
        self.favorite_user_id = favorite_user_id
        self.blog_id = blog_id
        self.image = image
        self.category_id = category_id


class BlogCategory(db.Model):
    __tablename__ = 'blog_category'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(140))
    blogs = db.relationship('Blog', backref='blogcategory', lazy='dynamic')
    otherblogs = db.relationship('OtherBlog', backref='blogcategory', lazy='dynamic')

    def __init__(self, category):
        self.category = category


class BlogComment(db.Model):
    __tablename__ = 'blog_comment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    comment = db.Column(db.Text)

    def __init__(self, user_id, blog_id, comment):
        self.user_id = user_id
        self.blog_id = blog_id
        self.comment = comment


class ChatChannel(db.Model):
    __tablename__ = 'chat_channel'

    id = db.Column(db.Integer, primary_key=True)
    channelname = db.Column(db.String(32))

    def __init__(self, channelname):
        self.channelname = channelname


class ChatMessage(db.Model):
    __tablename__ = 'chat_message'

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('chat_channel.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime, default=datetime.now(timezone('Asia/Tokyo')))
    message = db.Column(db.String(640))

    def __init__(self, date, channel_id, user_id, message):
        self.date = date
        self.channel_id = channel_id
        self.user_id = user_id
        self.message = message


class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64))
    title = db.Column(db.String(140))
    summary = db.Column(db.String(140))
    text = db.Column(db.Text)
    url = db.Column(db.String(140))
    image = db.Column(db.String(140))

    def __init__(self, category, title, summary, text, url, image):
        self.category = category
        self.title = title
        self.summary = summary
        self.text = text
        self.url = url
        self.image = image
