import smtplib
from email.mime.text import MIMEText

def send_email(recipient, subject, body):
    sender = "your-email@example.com"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    
    with smtplib.SMTP('smtp.your-email-provider.com', 587) as server:
        server.starttls()
        server.login(sender, "your-password")
        server.sendmail(sender, [recipient], msg.as_string())
