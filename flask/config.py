import os
basedir = os.path.abspath(os.path.dirname(__file__))

BASEDIR = basedir
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:.@localhost:3306/mytest"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'jsjfoiashjiofhja'