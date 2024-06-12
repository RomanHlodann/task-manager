from django.test import TestCase
from django.urls import reverse

from planner.models import TaskType, Worker


class LoginRequiredTaskTypeViewTest(TestCase):
    def test_login_required_task_type_list(self):
        response = self.client.get(reverse("planner:task-type-list"))
        self.assertEqual(response.status_code, 302)

    def test_login_required_task_type_create(self):
        response = self.client.get(reverse("planner:task-type-create"))
        self.assertEqual(response.status_code, 302)

    def test_login_required_task_type_update(self):
        response = self.client.get(reverse(
            "planner:task-type-update",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)

    def test_login_required_task_type_delete(self):
        response = self.client.get(reverse(
            "planner:task-type-delete",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)


class TaskTypeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_task_types = 4
        for task_type_id in range(number_of_task_types):
            TaskType.objects.create(
                name=f"Test{task_type_id}"
            )

    def setUp(self):
        self.tasktype = TaskType.objects.create(
                name="TaskType"
            )
        self.worker = Worker.objects.create_user(
            username="Test",
            password="1234",
            position=None
        )
        self.client.force_login(self.worker)

    def test_list_task_types(self):
        response = self.client.get(reverse("planner:task-type-list"))
        tasktypes = TaskType.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["tasktype_list"]), list(tasktypes))

    def test_filter_list_task_types(self):
        response = self.client.get(f"{reverse('planner:task-type-list')}?name=1") # noqa Q000
        self.assertEqual(len(response.context["tasktype_list"]), 1)

    def test_pagination_list_task_types(self):
        for task_type_id in range(10):
            TaskType.objects.create(
                name=f"Test2{task_type_id}"
            )
        response = self.client.get(reverse("planner:task-type-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["tasktype_list"]), 10)

        response = self.client.get(
            f"{reverse('planner:task-type-list')}?name=2&page=2" # noqa Q000
        )
        self.assertEqual(response.context["paginator"].num_pages, 2)

    def test_task_type_create_get(self):
        response = self.client.get(reverse("planner:task-type-create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "name")

    def test_task_type_create_post(self):
        data = {
            "name": "Bug fix"
        }
        self.client.post(reverse("planner:task-type-create"), data=data)
        new_task_type = TaskType.objects.get(name=data["name"])
        self.assertEqual(new_task_type.name, data["name"])

    def test_task_type_update_get(self):
        response = self.client.get(reverse(
            "planner:task-type-update",
            kwargs={"pk": self.tasktype.id}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.tasktype.name)

    def test_task_type_update_post(self):
        data = {
            "name": "New task type",
        }
        self.client.post(reverse(
            "planner:task-type-update",
            kwargs={"pk": self.tasktype.id}), data=data
        )
        TaskType.objects.get(name=data["name"])

    def test_task_type_delete_get(self):
        response = self.client.get(reverse(
            "planner:task-type-delete",
            kwargs={"pk": self.tasktype.id}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete task type")

    def test_task_type_delete_post(self):
        self.client.post(reverse(
            "planner:task-type-delete",
            kwargs={"pk": self.tasktype.id}
        ))
        ls = TaskType.objects.filter(name=self.tasktype.name)
        self.assertEqual(len(ls), 0)
