import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class ActivationLink(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        verbose_name='Ссылка для активации'
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    objects = models.Manager()

    class Meta:
        verbose_name = 'Ссылка для активации'
        verbose_name_plural = 'Ссылки для активации'

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse(
            'activate_user',
            kwargs={
                'user': self.user.username,
                'link': self.pk
            }
        )
