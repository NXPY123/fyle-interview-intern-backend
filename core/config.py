import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./store.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./test_store.sqlite3'  # Separate test database
    TESTING = True
    SQLALCHEMY_ECHO = False
