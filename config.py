import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://postgres:password@db/email_scheduler')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'devkey') 
    CELERY_BROKER_URL = os.getenv('REDIS_URI', 'redis://redis:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('REDIS_URI', 'redis://redis:6379/0')