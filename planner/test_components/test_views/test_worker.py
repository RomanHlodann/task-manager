from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from planner.models import Worker, Position


class LoginRequiredWorkerViewTest(TestCase):
    def test_login_required_worker_list(self):
        response = self.client.get(reverse("planner:worker-list"))
        self.assertEqual(response.status_code, 302)

    def test_login_required_worker_create(self):
        response = self.client.get(reverse("planner:worker-create"))
        self.assertEqual(response.status_code, 302)

    def test_login_required_worker_detail(self):
        response = self.client.get(reverse(
            "planner:worker-detail",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)

    def test_login_required_worker_update(self):
        response = self.client.get(reverse(
            "planner:worker-update",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)

    def test_login_required_worker_delete(self):
        response = self.client.get(reverse(
            "planner:worker-delete",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)


class WorkerViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_workers = 4
        position = Position.objects.create(
            name="Python Developer"
        )
        for driver_id in range(number_of_workers):
            Worker.objects.create(
                username=f"Username{driver_id}",
                password="12345",
                last_name="Last",
                position=position
            )

    def setUp(self):
        self.worker = Worker.objects.get(id=1)
        self.client.force_login(self.worker)

    def test_list_workers(self):
        response = self.client.get(reverse("planner:worker-list"))
        workers = Worker.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["worker_list"]), list(workers))

    def test_filter_list_workers(self):
        response = self.client.get(f"{reverse('planner:worker-list')}?username=1") # noqa Q000
        self.assertEqual(len(response.context["worker_list"]), 1)

    def test_pagination_list_workers(self):
        for worker_id in range(10):
            Worker.objects.create(
                username=f"Username 2{worker_id}",
                password="12345",
            )
        response = self.client.get(reverse("planner:worker-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["worker_list"]), 10)

        response = self.client.get(
            f"{reverse('planner:worker-list')}?username=2&page=2"  # noqa Q000
        )
        self.assertEqual(response.context["paginator"].num_pages, 2)

    def test_worker_detail_correct_data(self):
        response = self.client.get(reverse(
            "planner:worker-detail",
            kwargs={"pk": self.worker.id}
        ))
        self.assertContains(response, self.worker.username)
        self.assertContains(response, self.worker.position)

    def test_worker_create_get(self):
        response = self.client.get(reverse("planner:worker-create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First name")
        self.assertContains(response, "Last name")
        self.assertContains(response, "Username")
        self.assertContains(response, "Position")
        self.assertContains(response, "Email")
        self.assertContains(response, "Password")

    def test_worker_create_post(self):
        data = {
            "username": "Username202",
            "password1": "WhatWasThat2024",
            "password2": "WhatWasThat2024",
            "first_name": "First",
            "last_name": "Last",
        }
        self.client.post(reverse("planner:worker-create"), data=data)
        new_driver = get_user_model().objects.get(username=data["username"])
        self.assertEqual(new_driver.first_name, data["first_name"])
        self.assertEqual(new_driver.last_name, data["last_name"])

    def test_worker_update_get(self):
        response = self.client.get(reverse(
            "planner:worker-update",
            kwargs={"pk": self.worker.id}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.worker.position)

    def test_worker_update_post(self):
        data = {
            "username": self.worker.username,
            "first_name": "Firstname",
            "last_name": "Lastname",
            "email": "emailunique@gmail.com",
        }
        self.client.post(reverse(
            "planner:worker-update",
            kwargs={"pk": self.worker.id}
        ), data=data)
        new_driver = get_user_model().objects.get(
            id=self.worker.id
        )
        self.assertEqual(new_driver.first_name, data["first_name"])
        self.assertEqual(new_driver.last_name, data["last_name"])
        self.assertEqual(new_driver.email, data["email"])

    def test_worker_delete_get(self):
        response = self.client.get(reverse(
            "planner:worker-delete",
            kwargs={"pk": self.worker.id}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete worker")

    def test_driver_delete_post(self):
        self.client.post(reverse(
            "planner:worker-delete",
            kwargs={"pk": self.worker.id}
        ))
        ls = get_user_model().objects.filter(username=self.worker.username)
        self.assertEqual(len(ls), 0)
