from . import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(255), index = True)
    username = db.Column(db.String(255), index = True)
    email = db.Column(db.String(255), unique = True, index = True)
    password_hash = db.Column(db.String(255))   
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default = False)
    blog =  db.relationship('Blog', backref = 'user', lazy = "dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password property')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User {self.username}'

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), index = True)
    users = db.relationship('User', backref = 'role', lazy = 'dynamic')

class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    blog_id = db.Column(db.Integer,db.ForeignKey("blogs.id"))

class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key = True)
    image_path = db.Column(db.String())
    title = db.Column(db.String(255), index = True)
    post = db.Column(db.String(), index = True)
    time = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    photos = db.relationship('Photo', backref = 'blog', lazy = 'dynamic')
    comments = db.relationship('Comment', backref = 'blog', lazy = 'dynamic')
    
    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_blogs(cls):
        blog = Blog.query.order_by(Blog.time.desc()).all()
        return blog

    @classmethod
    def delete_blog(self, blog_id):
        comments = Comment.query.filter_by(blog_id = blog_id).delete()
        blog = Blog.query.filter_by(id = blog_id).delete()
        db.session.commit()

    
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), index = True)
    email = db.Column(db.String(50), index = True)
    post_comment = db.Column(db.String(255), index = True)
    time = db.Column(db.DateTime, default = datetime.now)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, id):
        comments = Comment.query.filter_by(blog_id = id).order_by(Comment.time.desc()).all()
        return comments

    @classmethod
    def delete_comment(cls, id):
        comment = Comment.query.filter_by(id = comment_id).delete()
        db.session.commit()
