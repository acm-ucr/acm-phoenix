# Global database instance.
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Global admin instance.
from flask_admin import Admin
admin = Admin()

# Global login manager.
from flask_login import LoginManager
login_manager = LoginManager()
