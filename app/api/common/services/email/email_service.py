import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailService:
    def __init__(self):
        # Set your sender email and password here
        self.sender_email = "searchcast.noreply@gmail.com"
        self.password = os.environ.get("EMAIL_PASSWORD")

    def send(self, email_data):
        receiver_email = email_data.get("to")
        subject = email_data.get("subject")
        html_body = email_data.get("html")

        if not (receiver_email and subject and html_body):
            print("Missing required parameters. Email not sent.")
            return

        # Create a message
        message = MIMEMultipart("alternative")
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Attach HTML body
        html_part = MIMEText(html_body, "html")
        message.attach(html_part)

        # Connect to the SMTP server (Gmail in this case)
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(self.sender_email, self.password)
            text = message.as_string()
            server.sendmail(self.sender_email, receiver_email, text)
