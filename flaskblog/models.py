from datetime import datetime
from flaskblog import db,login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})
    def get_reset_token_try(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_username': self.username, 'user_email':self.email, 'user_password':self.password})
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=300)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.password}', '{self.password}')"

    def __str__(self):
        return f"User('{self.username}', '{self.password}', '{self.password}')"
    
    @staticmethod
    def verify_reset_token_try(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            ret_user = s.loads(token, max_age=300)
            user = User(username=ret_user['user_username'], email=ret_user['user_email'], password=ret_user['user_password'])
            db.session.add(user)
            db.session.commit()
            return
        except:
            return None

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"