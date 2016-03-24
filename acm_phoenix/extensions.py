from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager

# Global database instance.
db = SQLAlchemy()

# Global admin instance.
admin = Admin()

# Global login manager.
login_manager = LoginManager()
