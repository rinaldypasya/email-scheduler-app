from . import db
import os

class ScheduledEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, nullable=False)
    recipients = db.Column(db.Text, nullable=False)
    email_subject = db.Column(db.String(255), nullable=False)
    email_content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False)
    sent = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<ScheduledEmail {self.recipients} - {self.timestamp}>"

    @property
    def recipient_list(self):
        return self.recipients.split(', ')

    @recipient_list.setter
    def recipient_list(self, emails):
        self.recipients = ','.join(emails)
        
    DEFAULT_TIMEZONE = os.getenv('DEFAULT_TIMEZONE', 'Asia/Singapore')

