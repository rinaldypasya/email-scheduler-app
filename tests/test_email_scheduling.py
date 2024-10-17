from app.models import ScheduledEmail
from datetime import datetime
import json
import pytz

def test_schedule_email(test_client, new_email, mock_celery_send_email_task):
    """
    Test that scheduling an email works and that the Celery task is triggered.
    """
    # Arrange - Create payload
    payload = {
        'event_id': new_email.event_id,
        'recipients': new_email.recipients,
        'email_subject': new_email.email_subject,
        'email_content': new_email.email_content,
        'timestamp': '2024-10-18 15:30:00',
        'timezone': 'Asia/Singapore'
    }

    # Act - Send POST request to schedule the email
    response = test_client.post('/api/save_emails', data=json.dumps(payload), content_type='application/json')

    # Assert - Check response
    assert response.status_code == 201
    assert b"Email scheduled successfully!" in response.data

    # Assert - Check if email was added to database
    scheduled_email = ScheduledEmail.query.first()
    assert scheduled_email.recipients == new_email.recipients
    assert scheduled_email.email_subject == new_email.email_subject

    # Assert - Celery task was triggered
    mock_celery_send_email_task.assert_called_once_with(scheduled_email.id)


def test_send_email_task(test_client, new_email, mocker):
    """
    Test that the send_email_task sends the email and marks it as sent in the database.
    """
    from app.tasks import send_email_task
    from app import db

    # Arrange - Add email to database
    db.session.add(new_email)
    db.session.commit()

    # Mock the actual send_email function to avoid sending real emails
    mock_send_email = mocker.patch('app.email_utils.send_email')

    # Act - Trigger the task manually
    send_email_task(new_email.id)

    # Assert - Check if the email was marked as sent
    sent_email = ScheduledEmail.query.get(new_email.id)
    assert sent_email.sent is True

    # Assert - The actual email sending function was called
    mock_send_email.assert_called_once()


def test_send_scheduled_emails(test_client, new_email, mock_celery_send_email_task):
    """
    Test the periodic task that triggers the sending task.
    """
    from app.tasks import schedule_email_task
    from app import db

    # Arrange - Set email scheduled time in the past
    new_email.timestamp = datetime.now().astimezone(pytz.timezone(ScheduledEmail.DEFAULT_TIMEZONE))
    db.session.add(new_email)
    db.session.commit()

    # Act - Run the periodic task
    schedule_email_task()

    # Assert - Celery task for sending the email is triggered
    scheduled_email = ScheduledEmail.query.first()
    mock_celery_send_email_task.assert_called_once_with(scheduled_email.id)