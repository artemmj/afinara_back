import os
import base64

from constance import config
from pysendpulse.pysendpulse import PySendPulse

from apps.application.models import Application

SENDPULSE_ID = os.environ.get('SENDPULSE_ID', None)
SENDPULSE_SECRET = os.environ.get('SENDPULSE_SECRET', None)
SENDPULSE_EMAIL_FROM = os.environ.get('SENDPULSE_EMAIL_FROM', None)


def send_email_feedback(appl_id: str):
    """Функция отправляет инфо по уже созданному объекту заявки (фидбека)."""
    appl = Application.objects.get(pk=appl_id)

    email_subject = 'Афинара :: Поступила новая заявка'
    email_body = (
        "Поступила новая заявка\n\n  "
        f"ФИО: {appl.name} \n  "
        f"Телефон: {appl.phone} \n  "
        f"E-mail: {appl.email} \n\n  "
        f"Комментарий: {appl.comment}\n\n"
    )
    html_email_body = (
        "Поступила новая заявка<br><br>  "
        f"  ФИО: {appl.name}<br>  "
        f"  Телефон: {appl.phone}<br>  "
        f"  E-mail: {appl.email}<br><br>  "
        f"Комментарий: {appl.comment}<br>"
    )

    attachments_bin = {}
    for file in appl.files.all():
        rb_file = open(file.file.path, 'rb')
        attachments_bin[rb_file.name.split("/")[-1]] = base64.b64encode(rb_file.read()).decode("utf-8")
        rb_file.close()

    SPApiProxy = PySendPulse(SENDPULSE_ID, SENDPULSE_SECRET, 'memcached')
    SPApiProxy.smtp_send_mail({
        'subject': email_subject,
        'html': html_email_body,
        'text': email_body,
        'from': {'name': 'service', 'email': SENDPULSE_EMAIL_FROM},
        'to': [
            {
                'name': config.email_feedback.split('@')[0],
                'email': config.email_feedback,
            },
        ],
        'attachments_binary': attachments_bin,
    })
