
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
CORS(app,supports_credential=True)

app.config.from_object('config')
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

from . import models,views