from flask_sqlalchemy import SQLAlchemy
from web import app

db = SQLAlchemy(app)
db.create_all()
