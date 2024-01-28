import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

dirname = os.path.dirname(__file__)
template_folder = os.path.join(dirname, "../email_templates")

conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get("SENDER_GMAIL"),
    MAIL_PASSWORD=os.environ.get("SENDER_GMAIL_PASSWORD"),
    MAIL_FROM=os.environ.get("SENDER_GMAIL"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="KanbanBoard forgot password",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
    TEMPLATE_FOLDER=template_folder
)


async def send_reset_password_mail(recipient_email, url, expire_in_minutes):
    template_body = {
        "url": url,
        "expire_in_minutes": expire_in_minutes
    }

    message = MessageSchema(
        subject="KanbanBoard forgot password",
        recipients=[recipient_email],
        template_body=template_body,
        subtype=MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="reset_password_email.html")
