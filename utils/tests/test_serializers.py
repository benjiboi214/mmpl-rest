from django.test import TestCase

from utils.serializers import ChoiceDisplayField, DefaultModelSerializer


class SerializerUtilTest(TestCase):

    def setUp(self):
        self.CHOICES = (
            ('A', 'A Display'),
            ('B', 'B Display')
        )

    def test_choice_field_shows_value_and_display(self):
        field = ChoiceDisplayField(self.CHOICES)
        self.assertEqual({
            'value': self.CHOICES[0][0],
            'display': self.CHOICES[0][1]
        }, field.to_representation(self.CHOICES[0][0]))

    def test_choices_field_set_on_serializer_model(self):
        serializer = DefaultModelSerializer()
        self.assertEqual(
            ChoiceDisplayField,
            serializer.serializer_choice_field)

    def test_none_return_on_custom_field(self):
        field = ChoiceDisplayField(self.CHOICES)
        self.assertEqual(None, field.to_representation(None))
