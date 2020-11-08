from app import db, login_manager

class Event(db.Model):
    __tablename__ = 'event'
    _id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), unique=False, nullable=False)
    from_date = db.Column(db.Date, unique=False, nullable=False)
    to_date = db.Column(db.Date, unique=False, nullable=False)
    theme = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    # user = db.Column(db.String(80), db.ForeignKey('user.id'))

class User(db.Model):
    __tablename__ = 'user'
    # id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    # unique=True
    email = db.Column(db.String(100), primary_key=True)

    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return True
        # return self.authenticated

    def is_active(self):
        return True
  
    def is_anonymous(self):
        return False
