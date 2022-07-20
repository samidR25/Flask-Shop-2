from datetime import datetime
from shop import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    description = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    image_file = db.Column(db.String(50), nullable=False, default='default.jpg')


    def __repr__(self):
        return f"Item('{self.title}', '{self.description}', '{self.price}')"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    password = db.Column(db.String(60), nullable=False)
    is_admin=db.Column(db.Boolean,nullable=False,default=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Basket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
