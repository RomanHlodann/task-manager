from django.db import IntegrityError
from django.test import TestCase

from planner.models import Position


class PositionModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Python Developer"
        )

    def test_name_label(self):
        field_label = self.position._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        max_length = self.position._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)

    def test_name_unique(self):
        try:
            Position.objects.create(
                name="Python Developer"
            )
            assert False
        except IntegrityError:
            assert True

    def test_position_str(self):
        expected_str = self.position.name
        self.assertEqual(expected_str, str(self.position))
