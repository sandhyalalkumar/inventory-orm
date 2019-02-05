from src.models import db
from src.models import ma
from src.models import bcrypt

class User(db.Model):
    """
    Create user table
    """

    __tablename__ = 'users'

    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(100))
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(100))
    address = db.Column(db.String(100))

    def __init__(self, data):
        self.username = data.get('username')
        self.password = self.__generate_hash(data.get('password'))
        self.firstname = data.get('firstname')
        self.lastname = data.get('lastname')
        self.email = data.get('email')
        self.address = data.get('address')

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def __repr__(self):
        return 'User: {}'.format(self.username)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'password', 'firstname', 'lastname', 'email', 'address')