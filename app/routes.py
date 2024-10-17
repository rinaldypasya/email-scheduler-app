from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .models import ScheduledEmail, db
from datetime import datetime
import pytz
from email_validator import validate_email, EmailNotValidError
from app.tasks import schedule_email_task

bp = Blueprint('main', __name__)

# Home page showing a list of scheduled emails
@bp.route('/')
def index():
    emails = ScheduledEmail.query.order_by(ScheduledEmail.timestamp).all()
    
    formatted_emails = []
    for email in emails:
        email.timestamp = email.timestamp.astimezone(pytz.timezone(ScheduledEmail.DEFAULT_TIMEZONE))
        formatted_emails.append(email)
        
    return render_template('index.html', emails=formatted_emails)

# Page to schedule a new email
@bp.route('/save_emails', methods=['POST', "GET"])
def save_emails():
    if request.method == 'POST':
        data = request.form
        recipients = [email.strip() for email in data['recipients'].split(',')]

        valid_recipients = []
        for email in recipients:
            try:
                valid = validate_email(email, check_deliverability=False).email
                valid_recipients.append(valid)
            except EmailNotValidError as e:
                return f"Invalid email address: {email}. Error: {str(e)}", 400

        user_timezone = pytz.timezone(data['timezone'])
        timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
        timestamp = user_timezone.localize(timestamp)

        timestamp_tz = timestamp.astimezone(pytz.timezone(ScheduledEmail.DEFAULT_TIMEZONE))

        new_email = ScheduledEmail(
            event_id=data['event_id'],
            email_subject=data['email_subject'],
            email_content=data['email_content'],
            timestamp=timestamp_tz,
        )
        new_email.recipient_list = valid_recipients
        db.session.add(new_email)
        db.session.commit()
        
        schedule_email_task.apply_async((new_email,), eta=timestamp_tz)

        return redirect(url_for('main.index'))
    return render_template('save_emails.html')
    
# API endpoint for scheduling emails
@bp.route('/api/save_emails', methods=['POST'])
def api_save_emails():
    data = request.get_json()
    recipients = [email.strip() for email in data['recipients'].split(',')]

    valid_recipients = []
    for email in recipients:
        try:
            valid = validate_email(email, check_deliverability=False).email
            valid_recipients.append(valid)
        except EmailNotValidError as e:
            return jsonify({"error": f"Invalid email address: {email}. Error: {str(e)}"}), 400

    user_timezone = pytz.timezone(data['timezone'])
    timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
    timestamp = user_timezone.localize(timestamp)

    timestamp_tz = timestamp.astimezone(pytz.timezone(ScheduledEmail.DEFAULT_TIMEZONE))

    new_email = ScheduledEmail(
        event_id=data['event_id'],
        email_subject=data['email_subject'],
        email_content=data['email_content'],
        timestamp=timestamp_tz,
    )
    new_email.recipient_list = valid_recipients
    db.session.add(new_email)
    db.session.commit()
    
    schedule_email_task.apply_async((new_email,), eta=timestamp_tz)

    return jsonify({"message": "Email scheduled successfully!"}), 201
