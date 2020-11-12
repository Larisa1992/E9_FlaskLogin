from app import db

class User(db.Model):
    __tablename__ = 'user'
    email = db.Column(db.String(100), primary_key=True)

    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True
  
    def is_anonymous(self):
        return False

class Event(db.Model):
    __tablename__ = 'event'
    _id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), db.ForeignKey('user.email'))
    from_date = db.Column(db.Date, unique=False, nullable=False)
    to_date = db.Column(db.Date, unique=False, nullable=False)
    theme = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)