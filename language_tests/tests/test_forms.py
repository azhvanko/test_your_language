from typing import Dict

from django.forms.models import inlineformset_factory
from django.test import TestCase

from language_tests.forms import QuestionAnswersInlineFormSet
from language_tests.models import QuestionAnswer, Question


class QuestionAnswersInlineFormSetTest(TestCase):
    fixtures = [
        'language_test_types',
        'answers',
        'questions',
    ]
    max_num = 4
    min_num = 4

    @staticmethod
    def create_data(
            number_forms: int,
            question_id: int,
            right_answers: tuple
    ) -> Dict[str, str]:
        data = {
            'questionanswer_set-TOTAL_FORMS': str(number_forms),
            'questionanswer_set-INITIAL_FORMS': '0',
            'questionanswer_set-MIN_NUM_FORMS': str(number_forms),
            'questionanswer_set-MAX_NUM_FORMS': str(number_forms),
        }
        for i in range(number_forms):
            data.update(
                {
                    f'questionanswer_set-{i}-answer': str(i + 1),
                    f'questionanswer_set-{i}-question': str(question_id),
                }
            )
            if i + 1 in right_answers:
                data[f'questionanswer_set-{i}-is_right_answer'] = 'on'
        return data

    @staticmethod
    def create_question(
            question: str,
            is_published: bool,
            test_type_id: int
    ) -> Question:
        return Question.objects.create(
            question=question,
            is_published=is_published,
            test_type_id=test_type_id
        )

    def test_formset(self):
        question = self.create_question('question ___ 0', True, 1)
        QuestionAnswersFormSet = inlineformset_factory(
            Question,
            QuestionAnswer,
            formset=QuestionAnswersInlineFormSet,
            fields='__all__',
            max_num=self.max_num,
            min_num=self.min_num
        )

        test_cases = (
            {'result': True, 'right_answers': (1,)},
            {'result': False, 'right_answers': tuple()},
            {'result': False, 'right_answers': (1, 2,)},
        )

        for test_case in test_cases:
            data = self.create_data(4, question.pk, test_case['right_answers'])
            formset = QuestionAnswersFormSet(instance=question, data=data)
            self.assertEqual(formset.max_num, formset.min_num)
            self.assertEqual(len(formset.forms), 4)
            self.assertEqual(test_case['result'], formset.is_valid())
