import datetime

from django import forms
from django.test import TestCase

from planner.models import Worker, Position, TaskType, Task
from planner.forms import (
    WorkerCreationForm,
    WorkerUpdateForm,
    TaskCreationForm,
)


class FormsTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Python Developer"
        )
        self.task_type = TaskType.objects.create(
            name="Bug fixing"
        )
        self.worker = Worker.objects.create(
                username="UsernameTest",
                password="12345",
                last_name="Last"
            )
        self.task = Task.objects.create(
            name=f"TestTask",
            description="///",
            deadline=datetime.date.today(),
            is_completed=False,
            priority='Low',
            task_type=self.task_type,
        )
        self.task.assignees.set([self.worker.id])

    def test_worker_creation(self):
        form_data = {
            "username": "Username202",
            "password1": "WhatWasThat2024",
            "password2": "WhatWasThat2024",
            "first_name": "First",
            "last_name": "Last",
            "email": "email@gmail.com",
            "position": None
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_worker_update(self):
        form_data = {
            "username": "Username202",
            "first_name": "NewName",
            "last_name": "Last",
            "assignees": self.worker.id,
            "email": "email@gmail.com",
            "position": self.position.id
        }
        form = WorkerUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])
        self.assertEqual(form.cleaned_data["first_name"], form_data["first_name"])
        self.assertEqual(form.cleaned_data["last_name"], form_data["last_name"])
        self.assertEqual(form.cleaned_data["email"], form_data["email"])
        self.assertEqual(form.cleaned_data["position"], self.position)

    def test_task_deadline_widget(self):
        form = TaskCreationForm()
        widget = form.fields["deadline"].widget
        self.assertTrue(isinstance(widget, forms.SelectDateWidget))

    def test_task_assignees_widget(self):
        form = TaskCreationForm()
        widget = form.fields["assignees"].widget
        self.assertTrue(isinstance(widget, forms.CheckboxSelectMultiple))

    def test_task_creation(self):
        form_data = {
            "name": "TestTask22",
            "description": "///",
            "deadline": datetime.date.today(),
            "is_completed": False,
            "priority": "Low",
            "assignees": [self.worker.id],
            "task_type": self.task_type.id
        }
        form = TaskCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], form_data["name"])
        self.assertEqual(form.cleaned_data["description"], form_data["description"])
        self.assertEqual(form.cleaned_data["is_completed"], form_data["is_completed"])
        self.assertEqual(form.cleaned_data["priority"], form_data["priority"])
        self.assertEqual(form.cleaned_data["is_completed"], form_data["is_completed"])
        self.assertEqual(form.cleaned_data["task_type"], self.task_type)
