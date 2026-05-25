from app.services.email_service import send_email

send_email(
    to_email="limbi.zangazanga@gmail.com",
    subject="Infodemiology Test",
    body="Email system working"
)