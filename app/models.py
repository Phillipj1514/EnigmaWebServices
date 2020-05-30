from . import db
from werkzeug.security import generate_password_hash


class Merchant(db.Model):
    __tablename__ = 'merchants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.Text)
    location = db.Column(db.String(100))
    logo = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    estimatedWaitTime = db.Column(db.Float)
    joined_on = db.Column(db.DateTime)

    def __init__(self, name, address, location, logo, email, password, estimatedWaitTime, joined_on):
        self.name = name
        self.address = address
        self.location = location
        self.logo = logo
        self.email = email
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.estimatedWaitTime = estimatedWaitTime
        self.joined_on = joined_on

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
    count = db.Column(db.Integer)
    waitTime = db.Column(db.Integer)

    def __init__(self, merchantID, queue, count, waitTime):
        self.merchantID = merchantID
        self.queue = queue
        self.count = count
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


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    merchantID = db.Column(db.Integer)
    queueID = db.Column(db.Integer)
    position = db.Column(db.Integer)
    code = db.Column(db.String(500))
    waitTime = db.Column(db.Integer)

    def __init__(self, merchantID, queueID, position, code, waitTime):
        self.merchantID = merchantID
        self.queueID = queueID
        self.position = position
        self.code = code
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
        return '<Customer %r>' % (self.id)



class JWTBlacklist(db.Model):
    __tablename__ = 'jwtspoils'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Text)

    def __init__(self, token):
        self.token = token

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
        return '<JWTSPOILS %r>' % (self.id)