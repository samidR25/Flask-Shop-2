from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__, template_folder='Templates',static_folder='static')

app.config['SECRET_KEY'] = 'edd9229339e5754427a7792fc79b51318395e93569165fa4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c2003538:Newport123@csmysql.cs.cf.ac.uk:3306/c2003538_Online_Shop'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


from shop import routes
from flask_admin import Admin
from shop.views import AdminView
from shop.models import User, Item
admin = Admin(app,name='Admin panel',template_mode='bootstrap3')
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Item, db.session))
