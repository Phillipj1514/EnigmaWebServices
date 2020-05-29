from . import db

class Profiles(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    email = db.Column(db.String(120),  unique=True)
    location = db.Column(db.String(100))
    biography = db.Column(db.Text)
    image = db.Column(db.Text)
    creation_date = db.Column(db.DateTime)

    def __init__(self, first_name, last_name, gender, email, location, biography, image, creation_date):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.email = email
        self.location = location
        self.biography = biography
        self.image = image
        self.creation_date = creation_date
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.id)
