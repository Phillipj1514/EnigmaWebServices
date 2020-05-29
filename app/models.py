from . import db

class Merchant(db.Model):
    __tablename__ = 'merchants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    logo = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    estimatedWaitTime = db.Column(db.Integer)

    def __init__(self, name, address, logo, email, password, estimatedWaitTime):
        self.name = name
        self.address = address
        self.logo = logo
        self.email = email
        self.password = password
        self.estimatedWaitTime = estimatedWaitTime

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
        return '<Merchant %r>' % (self.id)


class Line(db.Model):
    __tablename__ = 'lines'

    id = db.Column(db.Integer, primary_key=True)
    merchantID = db.Column(db.Integer)
    queue = db.Column(db.Text)
    waitTime = db.Column(db.Integer)

    def __init__(self, merchantID, queue, waitTime):
        self.merchantID = merchantID
        self.queue = queue
        self.waitTime = waitTime

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
        return '<Line %r>' % (self.id)