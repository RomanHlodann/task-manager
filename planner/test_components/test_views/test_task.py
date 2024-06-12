import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from planner.models import Worker, Task, TaskType


class LoginRequiredTaskViewTest(TestCase):
    def test_login_required_worker_list(self):
        response = self.client.get(reverse("planner:task-list"))
        self.assertEqual(response.status_code, 302)

    def test_login_required_worker_create(self):
        response = self.client.get(reverse("planner:task-create"))
        self.assertEqual(response.status_code, 302)

    def test_login_required_worker_detail(self):
        response = self.client.get(reverse(
            "planner:task-detail",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)

    def test_login_required_worker_update(self):
        response = self.client.get(reverse(
            "planner:task-update",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)

    def test_login_required_worker_delete(self):
        response = self.client.get(reverse(
            "planner:task-delete",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)

    def test_login_required_task_change_to_completed(self):
        response = self.client.get(reverse(
            "planner:task-change-to-completed",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)

    def test_login_required_task_remove_assignee(self):
        response = self.client.get(reverse(
            "planner:task-remove-assignee",
            kwargs={"task_id": 1, "assignee_id": 1}
        ))
        self.assertEqual(response.status_code, 302)


class TaskViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_tasks = 4
        number_of_assignees = 2
        task_type = TaskType.objects.create(
            name="Bug fixing"
        )

        assignees = []
        for driver_id in range(number_of_assignees):
            assignees.append(Worker.objects.create(
                username=f"Username{driver_id}",
                password="12345"
            ))

        for task_id in range(number_of_tasks):
            task = Task.objects.create(
                name=f"Task{task_id}",
                description="///",
                deadline=datetime.date.today(),
                is_completed=False,
                priority='Low',
                task_type=task_type,
            )
            task.assignees.set(assignees)

    def setUp(self):
        self.task = Task.objects.get(id=1)
        self.client.force_login(self.task.assignees.get(id=1))

    def test_list_tasks(self):
        response = self.client.get(reverse("planner:task-list"))
        tasks = Task.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["task_list"]), list(tasks))

    def test_filter_list_tasks(self):
        response = self.client.get(f"{reverse('planner:task-list')}?name=1")
        self.assertEqual(len(response.context["task_list"]), 1)

    def test_pagination_list_tasks(self):
        for task_id in range(10):
            Task.objects.create(
                name=f"Test2{task_id}",
                description=self.task.description,
                deadline=self.task.deadline,
                is_completed=self.task.is_completed,
                priority=self.task.priority,
                task_type=self.task.task_type,
            )
        response = self.client.get(reverse("planner:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["task_list"]), 5)

        response = self.client.get(
            f"{reverse('planner:task-list')}?name=2&page=2"  # noqa Q000
        )
        self.assertEqual(response.context["paginator"].num_pages, 3)

    def test_task_detail_correct_data(self):
        response = self.client.get(reverse(
            "planner:task-detail",
            kwargs={"pk": self.task.id}
        ))
        self.assertContains(response, self.task.name)
        self.assertContains(response, self.task.priority)
        self.assertContains(response, self.task.description)
        self.assertContains(response, self.task.is_completed)
        self.assertContains(response, self.task.task_type)

    def test_task_create_get(self):
        response = self.client.get(reverse("planner:task-create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Name")
        self.assertContains(response, "Description")
        self.assertContains(response, "Deadline")
        self.assertContains(response, "Task Type")
        self.assertContains(response, "Is completed")
        self.assertContains(response, "Priority")

    def test_worker_create_post(self):
        data = {
            "name": "Name",
            "description": "description",
            "deadline": self.task.deadline,
            "is_completed": True,
            "priority": "Urgent",
            "task_type": self.task.task_type.id,
            "assignees": [self.task.assignees.get(id=1).id]
        }
        self.client.post(reverse("planner:task-create"), data=data)
        new_task = Task.objects.get(name=data["name"])
        self.assertEqual(new_task.description, data["description"])
        self.assertEqual(new_task.is_completed, data["is_completed"])
        self.assertEqual(new_task.priority, data["priority"])

    def test_task_update_get(self):
        response = self.client.get(reverse(
            "planner:task-update",
            kwargs={"pk": self.task.id}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)
        self.assertContains(response, self.task.description)
        self.assertContains(response, self.task.priority)
        self.assertContains(response, self.task.task_type)

    def test_worker_update_post(self):
        data = {
            "name": self.task.name,
            "description": "description",
            "deadline": self.task.deadline,
            "is_completed": True,
            "priority": "Urgent",
            "task_type": self.task.task_type.id,
            "assignees": [self.task.assignees.get(id=1).id]
        }
        self.client.post(reverse(
            "planner:task-update",
            kwargs={"pk": self.task.id}
        ), data=data)
        new_task = Task.objects.get(
            id=self.task.id
        )
        self.assertEqual(new_task.description, data["description"])
        self.assertEqual(new_task.is_completed, data["is_completed"])
        self.assertEqual(new_task.priority, data["priority"])

    def test_worker_delete_get(self):
        response = self.client.get(reverse(
            "planner:task-delete",
            kwargs={"pk": self.task.id}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete task")

    def test_task_delete_post(self):
        self.client.post(reverse(
            "planner:task-delete",
            kwargs={"pk": self.task.id}
        ))
        ls = Task.objects.filter(name=self.task.name)
        self.assertEqual(len(ls), 0)

    def test_change_to_completed_task(self):
        self.client.post(reverse(
            "planner:task-change-to-completed",
            kwargs={"pk": self.task.id}
        ))
        task = Task.objects.get(id=self.task.id)
        self.assertTrue(task.is_completed)

    def test_remove_assignee_from_task(self):
        worker = Worker.objects.get(id=1)
        self.client.post(reverse(
            "planner:task-remove-assignee",
            kwargs={"task_id": self.task.id, "assignee_id": worker.id}
        ))
        task = Task.objects.get(id=self.task.id)
        self.assertFalse(task.assignees.all().contains(worker))
