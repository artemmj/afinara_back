from apps import app

from api.v1.application.services import send_email_feedback


@app.task()
def send_email_feedback_task(appl_id: str):
    """Оболочка для сервиса для асинхронного выполнения."""
    send_email_feedback(appl_id)
    return 'Задача по отправке письма выполнена.'
