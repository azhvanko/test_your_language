from typing import Dict, List

from language_tests.models import TestResult
from test_your_language.celery import app


@app.task
def save_user_answers(answers: List[Dict]) -> None:
    _answers = [
        TestResult(
            user_id=answer['user_id'],
            question_id=answer['question_id'],
            answer_id=answer['answer_id']
        )
        for answer in answers
    ]
    TestResult.objects.bulk_create(_answers)
