from flaskapp import db, login_manager, admin,bcrypt
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return signup.query.get(user_id)

class signup(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    articles = db.relationship('article', backref='author', lazy=True)
    def __repr__(self):
        return f"database('{self.username}', '{self.email}', '{self.password}')"

class article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    articletitle = db.Column(db.String(20), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('signup.id'), nullable=False)
    def __repr__(self):
        return f"database('{self.articletitle}', '{self.content}')"



class head(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    headtext = db.Column(db.String(150), unique=True, nullable=False)
    buttontext = db.Column(db.String(20), unique=True, nullable=False)
    phonenumber = db.Column(db.String(20), unique=True, nullable=False)



    def __repr__(self):
        return f"database('{self.main}')"



admin.add_view(ModelView(signup,db.session))
admin.add_view(ModelView(head,db.session))

