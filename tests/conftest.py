import pytest
import pytz
from app import create_app, db
from app.models import ScheduledEmail
from datetime import datetime

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(test_config=True)

    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'  # or 'memory://' for local testing
    flask_app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    
    # Flask provides a way to create a test client
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

@pytest.fixture(scope='function')
def new_email():
    return ScheduledEmail(
        event_id=1,
        recipients="test@example.com",
        email_subject="Test Subject",
        email_content="Test Body",
        timestamp=datetime(2024, 10, 18, 15, 30, 00).astimezone(pytz.timezone(ScheduledEmail.DEFAULT_TIMEZONE)),
    )

@pytest.fixture
def mock_celery_send_email_task(mocker):
    return mocker.patch('app.tasks.send_email_task.delay')
