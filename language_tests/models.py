from django.db import models


class LanguageTestType(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Тип теста'
    )
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    objects = models.Manager()

    class Meta:
        verbose_name = 'Тип теста'
        verbose_name_plural = 'Типы тестов'
        ordering = ['id', ]

    def __str__(self):
        return self.name
