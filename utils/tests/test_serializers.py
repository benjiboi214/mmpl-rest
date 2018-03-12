from django.test import TestCase

from utils.serializers import ChoiceDisplayField, DefaultModelSerializer


class SerializerUtilTest(TestCase):

    def test_choice_field_shows_value_and_display(self):
        CHOICES = (
            ('A', 'A Display'),
            ('B', 'B Display')
        )
        field = ChoiceDisplayField(CHOICES)
        self.assertEqual({
            'value': CHOICES[0][0],
            'display': CHOICES[0][1]
        }, field.to_representation(CHOICES[0][0]))

    def test_choices_field_set_on_serializer_model(self):
        serializer = DefaultModelSerializer()
        self.assertEqual(
            ChoiceDisplayField,
            serializer.serializer_choice_field)