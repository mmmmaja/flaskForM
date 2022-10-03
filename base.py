import os
from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=5)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sybirek123'
app.config['MYSQL_DB'] = 'flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)