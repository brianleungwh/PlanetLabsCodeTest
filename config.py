import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfiguration(object):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfiguration(BaseConfiguration):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.sqlite')
