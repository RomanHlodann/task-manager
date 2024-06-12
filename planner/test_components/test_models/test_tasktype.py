from django.db import IntegrityError
from django.test import TestCase

from planner.models import TaskType


class TaskTypeModelTest(TestCase):
    def setUp(self):
        self.tasktype = TaskType.objects.create(
            name="Bug fixing"
        )

    def test_name_label(self):
        field_label = self.tasktype._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        max_length = self.tasktype._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)

    def test_name_unique(self):
        try:
            TaskType.objects.create(
                name="Bug fixing"
            )
            assert False
        except IntegrityError:
            assert True

    def test_task_type_str(self):
        expected_str = self.tasktype.name
        self.assertEqual(expected_str, str(self.tasktype))
