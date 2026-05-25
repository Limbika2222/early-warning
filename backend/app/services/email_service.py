import smtplib

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"

SMTP_PORT = 587

SMTP_EMAIL = "limbi.zangazanga@gmail.com"

SMTP_PASSWORD = "kaemmqsgpscglfle"


def send_email(
    to_email: str,
    subject: str,
    body: str
):

    msg = MIMEMultipart()

    msg["From"] = SMTP_EMAIL

    msg["To"] = to_email

    msg["Subject"] = subject

    msg.attach(
        MIMEText(body, "plain")
    )

    server = smtplib.SMTP(
        SMTP_SERVER,
        SMTP_PORT
    )

    server.starttls()

    server.login(
        SMTP_EMAIL,
        SMTP_PASSWORD
    )

    server.send_message(msg)

    server.quit()