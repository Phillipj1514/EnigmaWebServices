from app import db 
from app.models import *
user = Merchant(first_name="Your name",last_name="Your last name", gender="male") 
db.session.add(user)
db.session.commit()