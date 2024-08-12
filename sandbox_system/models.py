import datetime
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
    password_hash = db.Column(db.String(128))
    administrator = db.Column(db.String(1))
    blog = db.relationship('Blog', backref = 'author', lazy = 'dynamic')

    def __init__(self, email, username, password, administrator):
        self.email = email
        self.username = username
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
    date = db.Column(db.Date, default = datetime.date.today())
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
    text = db.Column(db.Text)
    url = db.Column(db.String(140))
    image = db.Column(db.String(140))

    def __init__(self, title, summary, text, image):
        self.title = title
        self.summary = summary
        self.text = text
        self.image = image


class BlogCategory(db.Model):
    __tablename__ = 'blog_category'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(140))
    blogs = db.relationship('Blog', backref='blogcategory', lazy='dynamic')

    def __init__(self, category):
        self.category = category