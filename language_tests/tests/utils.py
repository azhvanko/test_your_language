from django.contrib.auth.models import User

from language_tests.models import (
    Answer,
    LanguageTestType,
    Question,
    QuestionAnswer,
    TestResult
)


class LanguageTestMixin:
    app_name = 'language_tests'
    default_number_answers = 4  # for 1 question
    default_number_questions = 20  # for 1 test type
    default_number_test_questions = 10  # for 1 test
    default_test_users_password = 'test_password'
    number_all_test_types = 10
    number_answers = number_all_test_types * default_number_answers
    number_published_test_types = number_all_test_types // 2
    number_questions = number_all_test_types * default_number_questions
    number_published_questions = int(number_questions * 0.8)
    number_question_answers = number_questions * default_number_answers

    fixtures = [
        'language_test_types',
        'questions',
        'answers',
        'question_answers',
        'users',
        'test_results',
    ]

    @staticmethod
    def create_answer(answer: str) -> Answer:
        return Answer.objects.create(answer=answer)

    @staticmethod
    def create_language_test_type(
            name: str,
            is_published: bool = True
    ) -> LanguageTestType:
        return LanguageTestType.objects.create(
            name=name,
            is_published=is_published
        )

    @staticmethod
    def create_question(
            question: str,
            test_type: str,
            is_published: bool = True
    ) -> Question:
        _test_type = LanguageTestType.objects.get(name=test_type)
        return Question.objects.create(
            question=question,
            is_published=is_published,
            test_type=_test_type
        )

    @staticmethod
    def create_question_answer(
            question: str,
            answer: str,
            is_right_answer: bool = False
    ) -> QuestionAnswer:
        _answer = Answer.objects.get(answer=answer)
        _question = Question.objects.get(question=question)
        return QuestionAnswer.objects.create(
            question=_question,
            answer=_answer,
            is_right_answer=is_right_answer
        )

    @staticmethod
    def create_test_result(
            user: str,
            question: str,
            answer: str
    ) -> TestResult:
        _user = User.objects.get(username=user)
        _question = Question.objects.get(question=question)
        _answer = Answer.objects.get(answer=answer)
        return TestResult.objects.create(
            user=_user,
            question=_question,
            answer=_answer
        )
