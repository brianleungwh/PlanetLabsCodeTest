import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
SQLALCHEMY_TEST_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False
