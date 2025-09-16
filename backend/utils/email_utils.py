import smtplib
from email.message import EmailMessage
from config import Config
import logging

logger = logging.getLogger(__name__)

def send_email(subject: str, html_body: str, to_email: str):
    # Dev fallback: print email if SMTP not configured
    if not Config.SMTP_HOST or not Config.SMTP_USERNAME:
        logger.warning("SMTP not configured — printing email to console")
        print(f"\n--- EMAIL TO: {to_email} ---\nSubject: {subject}\n\n{html_body}\n--- END EMAIL ---\n")
        return True

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = Config.EMAIL_FROM
    msg["To"] = to_email
    msg.set_content("This email requires HTML view")
    msg.add_alternative(html_body, subtype='html')

    try:
        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        logger.exception("Failed sending email")
        return False
