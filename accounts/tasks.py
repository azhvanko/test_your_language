from test_your_language.celery import app

from accounts.services import (
    send_activation_email as _send_activation_email,
    deactivate_user as _deactivate_user,
    delete_deactivated_accounts as _delete_deactivated_accounts
)


@app.task
def deactivate_user(username: str):
    _deactivate_user(username)


@app.task
def delete_deactivated_accounts():
    _delete_deactivated_accounts()


@app.task
def send_activation_email(user_id: int, email: str, site: str, reactivate: bool):
    _send_activation_email(user_id, email, site, reactivate)
