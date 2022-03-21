from flask import Flask

from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Secret_Key'
#3989053618eed15920665e7d9a2829b0
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/User/Desktop/New_pro/flaskapp/database.db'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'umarovfeqan@gmail.com'
app.config['MAIL_PASSWORD'] = 'Feqan1997Qafqaz9779'
#cqiubfezunmdnhqy
app.config['MAIL_USE_SSL'] = True


db= SQLAlchemy(app)
bcrypt = Bcrypt(app)
admin = Admin(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskapp import routes