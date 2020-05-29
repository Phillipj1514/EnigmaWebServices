from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = "ef322fmewfimsfeoefofdswf3o4jfemds"
app.config['UPLOAD_FOLDER'] = "./app/static/uploads"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://zuxrrphqzfszhc:4ec9b37c196ed0cfe7229b8b754e4d6f6b391ab0b22e07d7be92f982539ea91a@ec2-35-169-254-43.compute-1.amazonaws.com:5432/d4okef153bvb0c"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

app.config.from_object(__name__)

from app import views
# testing commits