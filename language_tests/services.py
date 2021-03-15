from typing import Dict, List, NamedTuple, Optional, Union

from django.db.models import QuerySet

from language_tests.models import QuestionAnswer, Question, TestResult


class LanguageQuestion(NamedTuple):
    question_id: int
    question: List[str]
    answers: Dict[int, str]


def generate_questions_list(
        test_type_id: int,
        user_id: Optional[int],
        number_questions: int = 10
) -> List[LanguageQuestion]:
    questions = Question.objects.prefetch_related(
        'answers'
    ).filter(
        test_type_id=test_type_id,
        is_published=True
    ).only(
        'id',
        'question'
    )

    prev_used_questions = TestResult.objects.values(
        'question'
    ).filter(
        user_id=user_id,
        question__in=questions
    ).distinct()

    # order_by('?') queries may be expensive and slow, depending on the database backend you’re using.
    # https://books.agiliq.com/projects/django-orm-cookbook/en/latest/random.html
    if not user_id:
        return _get_questions(
            questions.order_by('?'),
            [],
            number_questions
        )

    if questions.count() - prev_used_questions.count() >= number_questions:
        return _get_questions(
            questions,
            prev_used_questions,
            number_questions
        )

    return _get_questions(
        questions.order_by('?'),
        [],
        number_questions
    )


def get_right_answers(
        answers: Dict[str, str],
        user_id: Optional[int]
) -> Dict[int, int]:
    _answers = {}
    for key, value in answers.items():
        value = int(value) if value else 0
        _answers[int(key)] = value

    questions = QuestionAnswer.objects.values(
        'question_id',
        'answer_id',
        'is_right_answer'
    ).filter(
        question_id__in=[i for i in _answers.keys()]
    )

    result = {}
    valid_answers = []
    for item in questions:
        if user_id and _answers[item['question_id']] == item['answer_id']:
            valid_answers.append(
                TestResult(
                    question_id=item['question_id'],
                    answer_id=item['answer_id'],
                    user_id=user_id
                )
            )
        if item['is_right_answer']:
            result[item['question_id']] = item['answer_id']

    if user_id:
        TestResult.objects.bulk_create(valid_answers)

    return result


def _get_questions(
        all_questions: QuerySet,
        prev_used_questions: Union[List, QuerySet],
        limit: int
) -> List[LanguageQuestion]:
    questions = all_questions.exclude(id__in=prev_used_questions)[:limit]

    result = []

    for question in questions:
        answers = {
            answer.pk: answer.answer
            for answer in question.answers.all()
        }
        result.append(
            LanguageQuestion(
                question_id=question.pk,
                question=[i for i in question.question.strip().split()],
                answers=answers
            )
        )

    return result
