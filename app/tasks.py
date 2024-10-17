from celery import Celery
from app import db
from app.email_utils import send_email
import os

celery = Celery('tasks', broker=os.getenv('REDIS_URI', 'redis://redis:6379/0'))

@celery.task
def send_email_task(email):
    """Task to send an individual email."""
    if email and not email.sent:
        # Send an email to each recipient
        for recipient in email.recipient_list:
            send_email(recipient, email.email_subject, email.email_content)

        email.sent = True
        db.session.commit()

@celery.task
def schedule_email_task(email):
    send_email_task.delay(email)