from django.test import TestCase
from django.urls import reverse

from planner.models import Position, Worker


class LoginRequiredPositionViewTest(TestCase):
    def test_login_required_position_list(self):
        response = self.client.get(reverse("planner:position-list"))
        self.assertEqual(response.status_code, 302)

    def test_login_required_position_create(self):
        response = self.client.get(reverse("planner:position-create"))
        self.assertEqual(response.status_code, 302)

    def test_login_required_position_update(self):
        response = self.client.get(reverse(
            "planner:position-update",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)

    def test_login_required_position_delete(self):
        response = self.client.get(reverse(
            "planner:position-delete",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)


class PositionViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_positions = 4
        for position_id in range(number_of_positions):
            Position.objects.create(
                name=f"Test{position_id}"
            )

    def setUp(self):
        self.position = Position.objects.create(
                name="Python Developer"
            )
        self.worker = Worker.objects.create_user(
            username="Test",
            password="1234",
            position=None
        )
        self.client.force_login(self.worker)

    def test_list_positions(self):
        response = self.client.get(reverse("planner:position-list"))
        positions = Position.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["position_list"]), list(positions))

    def test_filter_list_positions(self):
        response = self.client.get(f"{reverse('planner:position-list')}?name=1") # noqa Q000
        self.assertEqual(len(response.context["position_list"]), 1)

    def test_pagination_list_positions(self):
        for position_id in range(10):
            Position.objects.create(
                name=f"Test2{position_id}"
            )
        response = self.client.get(reverse("planner:position-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["position_list"]), 10)

        response = self.client.get(
            f"{reverse('planner:position-list')}?name=2&page=2" # noqa Q000
        )
        self.assertEqual(response.context["paginator"].num_pages, 2)

    def test_position_create_get(self):
        response = self.client.get(reverse("planner:position-create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "name")

    def test_position_create_post(self):
        data = {
            "name": "Java Developer"
        }
        self.client.post(reverse("planner:position-create"), data=data)
        new_position = Position.objects.get(name=data["name"])
        self.assertEqual(new_position.name, data["name"])

    def test_position_update_get(self):
        response = self.client.get(reverse(
            "planner:position-update",
            kwargs={"pk": self.position.id}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.position.name)

    def test_position_update_post(self):
        data = {
            "name": "New position",
        }
        self.client.post(reverse(
            "planner:position-update",
            kwargs={"pk": self.position.id}), data=data
        )
        Position.objects.get(name=data["name"])

    def test_position_delete_get(self):
        response = self.client.get(reverse(
            "planner:position-delete",
            kwargs={"pk": self.position.id}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete position")

    def test_position_delete_post(self):
        self.client.post(reverse(
            "planner:position-delete",
            kwargs={"pk": self.position.id}
        ))
        ls = Position.objects.filter(name=self.position.name)
        self.assertEqual(len(ls), 0)
