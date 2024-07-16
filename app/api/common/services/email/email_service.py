import os
import resend


class EmailService:
    def __init__(self):
        resend.api_key = os.environ["RESEND_API_KEY"]

    def send(self, email_data):
        receiver_email = email_data.get("to")
        subject = email_data.get("subject")
        html_body = email_data.get("html")

        if not (receiver_email and subject and html_body):
            print("Missing required parameters. Email not sent.")
            return

        params: resend.Emails.SendParams = {
            "from": "searchcast.noreply@gmail.com",
            "to": [receiver_email],
            "subject": subject,
            "html": html_body,
        }

        try:
            email = resend.Emails.send(params)
            print("Email sent successfully:", email)
        except Exception as e:
            print(f"Failed to send email. Error: {e}")
