from hotelbooking.celery import app
from .utils import send_activation_code


@app.task
def send_activation_code_celery(email, activation_code):
    send_activation_code(email, activation_code)
