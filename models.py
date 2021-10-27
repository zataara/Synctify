from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
        db.app = app
        db.init_app(app)


class User(db.Model):
    '''Database model for Users'''

    __tablename__ = 'user'

    def __repr__(self):
        
        u = self
        return f'<User {u.id} username={u.username} name={first_name} {last_name}>'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    email = db.Column(db.String(20),
                            nullable=False,
                            unique=True)
    password = db.Column(db.String,
                            nullable=False)
    first_name = db.Column(db.String(30),
                            nullable=False)
    last_name = db.Column(db.String(30),
                            nullable=False)
    state = db.Column(db.String(2),
                            nullable=False) 

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user with a hashed password and return that user"""
        
        hashed = bcrypt.generate_password_hash(password)
        #turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode('utf8')
        new_user = cls(
            username=username,
            password=hashed_utf8,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        db.session.add(new_user)
        return new_user

    @classmethod
    def authenticate(cls, username, pwd):
        '''Check username and password against hashed password stored in db'''

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password,pwd):
            return u
        else:
            return False



class HomeUsage(db.Model):
    '''Database Model for Home Usage'''

    __tablename__ = 'HomeUsage'

    def __repr__(self):
        
        h = self
        return f'<HomeUsage {h.id} username={h.user_id} usage={h.usage}>'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    user_id = db.Column(db.Integer(20),
                            db.ForeignKey('user.username'),
                            nullable=False,)
    month_name = db.Column(db.String(50),
                            nullable=False)
    usage = db.Column(db.Integer(10),
                            nullable=False)



