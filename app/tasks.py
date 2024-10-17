from celery import Celery
from app import db
from app.email_utils import send_email
import os
from app.models import ScheduledEmail
from datetime import datetime
import pytz

celery = Celery('tasks', broker=os.getenv('REDIS_URI', 'redis://redis:6379/0'))

@celery.task
def send_email_task(email_id):
    """Task to send an individual email."""
    email = ScheduledEmail.query.get(email_id)
    
    if email and not email.sent:
        # Send an email to each recipient
        for recipient in email.recipient_list:
            send_email(recipient, email.email_subject, email.email_content)

        email.sent = True
        db.session.commit()

@celery.task
def schedule_email_task():
    """Task that runs periodically to send scheduled emails."""
    now = datetime.now().astimezone(pytz.timezone(ScheduledEmail.DEFAULT_TIMEZONE))
    unsent_emails = ScheduledEmail.query.filter(ScheduledEmail.timestamp <= now, ScheduledEmail.sent == False).all()
    
    for email in unsent_emails:
        send_email_task.delay(email.id)