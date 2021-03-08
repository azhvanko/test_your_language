from django.db import models
from django.urls import reverse


class LanguageTestType(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Тип теста'
    )
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')

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


class Question(models.Model):
    question = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Вопрос'
    )
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')
    test_type = models.ForeignKey(
        LanguageTestType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Тип теста',
        related_name='questions'
    )
    answers = models.ManyToManyField(
        Answer,
        through='QuestionAnswer',
        through_fields=('question', 'answer')
    )

    objects = models.Manager()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['question', ]

    def __str__(self):
        return self.question


class QuestionAnswer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='Вопрос'
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        verbose_name='Ответ на вопрос'
    )
    is_right_answer = models.BooleanField(
        default=False,
        verbose_name='Правильный ответ'
    )

    objects = models.Manager()

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('question', 'answer',),
                name='%(app_label)s_%(class)s_question_answer_constraint'
            ),
            models.UniqueConstraint(
                fields=('question',),
                condition=models.Q(is_right_answer=True),
                name='%(app_label)s_%(class)s_question_is_right_answer_constraint'
            ),
        )
        ordering = ['question', ]
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопросы'

    def __str__(self):
        return f'{self.question} | {str(self.answer)} | {self.is_right_answer}'
