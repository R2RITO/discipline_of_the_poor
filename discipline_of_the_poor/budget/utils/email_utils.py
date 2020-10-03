import yagmail
from django.conf import settings


def send_email(recipient, subject, text_body, html_body):
    yag = yagmail.SMTP(user=settings.DOTP_EMAIL)
    yag.send(
        to=recipient,
        subject=subject,
        contents=html_body,
    )
