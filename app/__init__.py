from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = "ef322fmewfimsfeoefofdswf3o4jfemds"
app.config['UPLOAD_FOLDER'] = "./app/static/uploads"
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://shuhstvneemlya:b08e53709a5874baddb0d8bc892dd15ee564128a9eb9218157fd5d9698e4f3a3@ec2-52-207-93-32.compute-1.amazonaws.com:5432/d55oknimbd2j6s"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#db = SQLAlchemy(app)

app.config.from_object(__name__)

from app import views
# testing commits