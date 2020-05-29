from flask import Flask
# from flask_wtf.csrf import CSRFProtect 
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = 'A$EtgV//-ZfOos4~z=1!,u9i-7h@g05pgq?Ca,>8A9}ZKdg}A!Xurkv/IfCjU:+'
app.config['UPLOAD_FOLDER'] = "./app/static/uploads"

#sql alchemy database heconfiguration
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://zuxrrphqzfszhc:4ec9b37c196ed0cfe7229b8b754e4d6f6b391ab0b22e07d7be92f982539ea91a@ec2-35-169-254-43.compute-1.amazonaws.com:5432/d4okef153bvb0c"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

app.config.from_object(__name__)

from app import views