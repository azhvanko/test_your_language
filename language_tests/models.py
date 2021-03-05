from django.db import models
from django.urls import reverse


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

    def get_absolute_url(self):
        return reverse('language_test_preview', kwargs={'pk': self.pk})


class Answer(models.Model):
    answer = models.CharField(max_length=64, unique=True, verbose_name='Ответ')

    objects = models.Manager()

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['answer', ]

    def __str__(self):
        return self.answer
