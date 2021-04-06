from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.exceptions import (
    ObjectDoesNotExist,
    ValidationError
)
from django.core.mail import send_mail
from pytz import timezone

from accounts.models import ActivationLink
from test_your_language.settings import (
    ACTIVATION_LINK_LIFETIME,
    EMAIL_HOST_USER,
    TIME_ZONE
)


def activate_email(link: str) -> str:
    try:
        activation_link = ActivationLink.objects.select_related('user').get(id=link)
    except (ObjectDoesNotExist, ValidationError):
        flag = False
    else:
        tz = timezone(TIME_ZONE)
        _timedelta = (datetime.now(tz) - activation_link.user.date_joined)
        flag = _timedelta.total_seconds() < ACTIVATION_LINK_LIFETIME
        if not flag:
            activation_link.user.delete()

    if flag:
        _activate_email(activation_link)
        return 'Ваша учётная запись была успешно активирована.'
    return (
        'При активации вашей учётной записи произошла ошибка. '
        'Пожалуйста, попробуйте позднее.'
    )


def deactivate_user(username: str) -> None:
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        pass
    else:
        user.is_active = False
        user.save(update_fields=['is_active', ])


def delete_deactivated_accounts() -> None:
    tz = timezone(TIME_ZONE)
    date = datetime.now(tz) - timedelta(seconds=ACTIVATION_LINK_LIFETIME)
    User.objects.filter(
        is_active=False,
        date_joined__lt=date,
        last_login=None
    ).delete()


def send_activation_email(
        user_id: int,
        email: str,
        site: str,
        reactivate: bool
) -> None:
    link = _create_activation_link(user_id, site)
    reactivate_message = 'повторной ' if reactivate else ''
    message = (
        f'Добрый день!\n\n'
        f'Ваш email был использован при регистрации на сайте {site}.\n'
        f'Для {reactivate_message}активации вашей учетной записи - перейдите '
        f'по ссылке ниже.\n\n{link}\n\n'
    )

    send_mail(
        subject='Подтверждение email',
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email, ],
        fail_silently=False
    )


def _create_activation_link(user_id: int, site: str) -> str:
    activation_link = ActivationLink(user_id=user_id)
    activation_link.save()

    return f'https://{site}{activation_link.get_absolute_url()}'


def _activate_email(activation_link: ActivationLink) -> None:
    activation_link.user.is_active = True
    activation_link.user.save(update_fields=['is_active', ])
    activation_link.delete()
