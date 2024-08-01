import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uggghardcodedsecret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///identity_provider.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
