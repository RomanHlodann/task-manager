import datetime

from django.db import IntegrityError
from django.test import TestCase

from planner.models import Task, TaskType, Worker, Position


class TaskModelTest(TestCase):
    def setUp(self):
        self.worker = Worker.objects.create_user(
            username="Test",
            password="1234",
            position=Position.objects.create(
                name="Python Developer"
            )
        )
        self.task = Task.objects.create(
            name="Create home page",
            description="This should be a home page for planner",
            deadline=datetime.date.today(),
            is_completed=False,
            priority='Low',
            task_type=TaskType.objects.create(
                name="Site layout"
            ),
        )
        self.task.assignees.set([self.worker])

    def test_name_label(self):
        field_label = self.task._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        max_length = self.task._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)

    def test_name_unique(self):
        try:
            Position.objects.create(
                name="Python Developer"
            )
            assert False
        except IntegrityError:
            assert True

    def test_description_label(self):
        field_label = self.task._meta.get_field("description").verbose_name
        self.assertEqual(field_label, "description")

    def test_description_max_length(self):
        max_length = self.task._meta.get_field("description").max_length
        self.assertEqual(max_length, 255)

    def test_deadline_label(self):
        field_label = self.task._meta.get_field("deadline").verbose_name
        self.assertEqual(field_label, "deadline")

    def test_priority_label(self):
        field_label = self.task._meta.get_field("priority").verbose_name
        self.assertEqual(field_label, "priority")

    def test_priority_max_length(self):
        max_length = self.task._meta.get_field("priority").max_length
        self.assertEqual(max_length, 6)

    def test_priority_choices(self):
        URGENT = 'Urgent'
        LOW = 'Low'
        MEDIUM = 'Medium'
        HIGH = 'High'

        PRIORITY_CHOICES = (
            (LOW, 'Low'),
            (MEDIUM, 'Medium'),
            (HIGH, 'High'),
            (URGENT, 'Urgent'),
        )

        choices = self.task._meta.get_field("priority").choices
        self.assertEqual(choices, PRIORITY_CHOICES)

    def test_task_type_label(self):
        field_label = self.task._meta.get_field("task_type").verbose_name
        self.assertEqual(field_label, "task type")

    def test_assignees_label(self):
        field_label = self.task._meta.get_field("assignees").verbose_name
        self.assertEqual(field_label, "assignees")

    def test_task_str(self):
        expected_str = (f"{self.task.name}. "
                        f"Priority: {self.task.priority}")
        self.assertEqual(expected_str, str(self.task))
