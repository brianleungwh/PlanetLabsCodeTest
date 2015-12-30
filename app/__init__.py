from flask import Flask
from models import db

app = Flask(__name__)
app.config.from_object('config.BaseConfiguration')
db.init_app(app)

from app import controllers, models
