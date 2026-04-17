import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()  

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
