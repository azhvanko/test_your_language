from django.test import TestCase

from language_tests.models import (
    Answer,
    LanguageTestType,
    Question,
    QuestionAnswer
)


class LanguageTestMixin:
    app_name = 'language_tests'
    default_number_answers = 4  # for 1 question
    number_all_test_types = 10
    number_answers = number_all_test_types * default_number_answers
    number_published_test_types = number_all_test_types // 2
    number_questions = number_all_test_types * 20
    number_published_questions = int(number_questions * 0.8)
    number_question_answers = number_questions * default_number_answers

    fixtures = [
        'language_test_types',
        'questions',
        'answers',
        'question_answers',
    ]

    @staticmethod
    def create_language_test_type(name: str) -> LanguageTestType:
        return LanguageTestType.objects.create(name=name)

    @staticmethod
    def create_answer(answer: str) -> Answer:
        return Answer.objects.create(answer=answer)

    @staticmethod
    def create_question(question: str, test_type: str) -> Question:
        _test_type = LanguageTestType.objects.get(name=test_type)
        return Question.objects.create(
            question=question,
            is_published=True,
            test_type=_test_type
        )

    @staticmethod
    def create_question_answer(
            question: str,
            answer: str,
            is_right_answer: bool
    ) -> QuestionAnswer:
        _answer = Answer.objects.get(answer=answer)
        _question = Question.objects.get(question=question)
        return QuestionAnswer.objects.create(
            question=_question,
            answer=_answer,
            is_right_answer=is_right_answer
        )


class LanguageTestTypeTest(LanguageTestMixin, TestCase):

    def test_object_creation(self):
        language_test_type = self.create_language_test_type('test_type_0')
        self.assertEqual(language_test_type.name, 'test_type_0')
        self.assertTrue(language_test_type.is_published)

    def test_objects_creation(self):
        all_test_types = LanguageTestType.objects.all()
        published_test_types = all_test_types.filter(is_published=True)
        self.assertEqual(len(all_test_types), self.number_all_test_types)
        self.assertEqual(len(published_test_types), self.number_published_test_types)

    def test_name(self):
        language_test_type = LanguageTestType.objects.get(id=1)
        field_label = language_test_type._meta.get_field('name').verbose_name
        max_length = language_test_type._meta.get_field('name').max_length
        unique = language_test_type._meta.get_field('name').unique
        self.assertEqual(field_label, 'Тип теста')
        self.assertEqual(max_length, 128)
        self.assertTrue(unique)

    def test_is_published(self):
        language_test_type = LanguageTestType.objects.get(id=1)
        field_label = language_test_type._meta.get_field('is_published').verbose_name
        default = language_test_type._meta.get_field('is_published').default
        self.assertEqual(field_label, 'Опубликован')
        self.assertTrue(default)

    def test_meta(self):
        self.assertEqual(LanguageTestType._meta.verbose_name, 'Тип теста')
        self.assertEqual(LanguageTestType._meta.verbose_name_plural, 'Типы тестов')

    def test_str_method(self):
        language_test_type = LanguageTestType.objects.get(id=1)
        self.assertEqual(str(language_test_type), 'test_type_1')

    def test_get_absolute_url(self):
        language_test_type = LanguageTestType.objects.get(id=1)
        self.assertEqual(language_test_type.get_absolute_url(), '/tests/1/')


class AnswerTest(LanguageTestMixin, TestCase):

    def test_object_creation(self):
        answer = self.create_answer('answer_0')
        self.assertEqual(answer.answer, 'answer_0')

    def test_objects_creation(self):
        all_answers = Answer.objects.all()
        self.assertEqual(len(all_answers), self.number_answers)

    def test_answer(self):
        answer = Answer.objects.get(id=1)
        field_label = answer._meta.get_field('answer').verbose_name
        max_length = answer._meta.get_field('answer').max_length
        unique = answer._meta.get_field('answer').unique
        self.assertEqual(field_label, 'Ответ')
        self.assertEqual(max_length, 64)
        self.assertTrue(unique)

    def test_meta(self):
        self.assertEqual(Answer._meta.verbose_name, 'Ответ')
        self.assertEqual(Answer._meta.verbose_name_plural, 'Ответы')

    def test_str_method(self):
        answer = Answer.objects.get(id=1)
        self.assertEqual(str(answer), 'answer_1')


class QuestionTest(LanguageTestMixin, TestCase):

    def test_object_creation(self):
        question = self.create_question('question ___ 0', 'test_type_1')
        self.assertEqual(question.question, 'question ___ 0')
        self.assertEqual(question.test_type.name, 'test_type_1')
        self.assertTrue(question.is_published)

    def test_objects_creation(self):
        all_questions = Question.objects.all()
        active_questions = all_questions.filter(is_published=True)
        self.assertEqual(len(all_questions), self.number_questions)
        self.assertEqual(len(active_questions), self.number_published_questions)

    def test_question(self):
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('question').verbose_name
        max_length = question._meta.get_field('question').max_length
        unique = question._meta.get_field('question').unique
        self.assertEqual(field_label, 'Вопрос')
        self.assertEqual(max_length, 256)
        self.assertTrue(unique)

    def test_is_published(self):
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('is_published').verbose_name
        default = question._meta.get_field('is_published').default
        self.assertEqual(field_label, 'Опубликован')
        self.assertTrue(default)

    def test_test_type(self):
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('test_type').verbose_name
        null = question._meta.get_field('test_type').null
        fk = question._meta.get_field('test_type').many_to_one
        self.assertEqual(question.test_type_id, 1)
        self.assertEqual(field_label, 'Тип теста')
        self.assertTrue(null)
        self.assertTrue(fk)

    def test_answers(self):
        question = Question.objects.get(id=1)
        m2m = question._meta.get_field('answers').many_to_many
        self.assertTrue(m2m)

    def test_meta(self):
        self.assertEqual(Question._meta.verbose_name, 'Вопрос')
        self.assertEqual(Question._meta.verbose_name_plural, 'Вопросы')

    def test_str_method(self):
        question = Question.objects.get(id=1)
        self.assertEqual(str(question), 'question ___ 1')


class QuestionAnswerTest(LanguageTestMixin, TestCase):

    def test_object_creation(self):
        test_type = self.create_language_test_type('test_type_0')
        question = self.create_question('question ___ 0', test_type.name)
        answer = self.create_answer('answer_0')
        question_answer = self.create_question_answer(
            question=question.question,
            answer=answer.answer,
            is_right_answer=True
        )
        self.assertEqual(question_answer.question.question, 'question ___ 0')
        self.assertEqual(question_answer.answer.answer, 'answer_0')
        self.assertTrue(question_answer.is_right_answer)

    def test_objects_creation(self):
        all_question_answers = QuestionAnswer.objects.all()
        right_answers = all_question_answers.filter(is_right_answer=True)
        self.assertEqual(len(all_question_answers), self.number_question_answers)
        self.assertEqual(
            len(right_answers),
            self.number_question_answers // self.default_number_answers
        )

    def test_question(self):
        question_answer = QuestionAnswer.objects.get(id=1)
        fk = question_answer._meta.get_field('question').many_to_one
        self.assertTrue(fk)

    def test_answer(self):
        question_answer = QuestionAnswer.objects.get(id=1)
        fk = question_answer._meta.get_field('answer').many_to_one
        self.assertTrue(fk)

    def test_is_right_answer(self):
        question_answer = QuestionAnswer.objects.get(id=1)
        field_label = question_answer._meta.get_field('is_right_answer').verbose_name
        default = question_answer._meta.get_field('is_right_answer').default
        self.assertEqual(field_label, 'Правильный ответ')
        self.assertFalse(default)

    def test_meta(self):
        self.assertEqual(len(QuestionAnswer._meta.constraints), 2)
        self.assertEqual(QuestionAnswer._meta.verbose_name, 'Ответ на вопрос')
        self.assertEqual(
            QuestionAnswer._meta.verbose_name_plural,
            'Ответы на вопросы'
        )

    def test_str_method(self):
        question_answer = QuestionAnswer.objects.get(id=1)
        self.assertEqual(str(question_answer), 'question ___ 1 | answer_1 | True')
