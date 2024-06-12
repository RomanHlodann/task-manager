from django.test import TestCase

from planner.models import Worker, Position


class DriverModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
                name="Python Developer"
            )
        self.worker = Worker.objects.create_user(
            username="Test",
            password="1234",
            position=self.position
        )

    def test_class_verbose_name(self):
        verbose_name = self.worker._meta.verbose_name
        self.assertEqual(verbose_name, "worker")

    def test_class_verbose_name_plural(self):
        verbose_name_plural = self.worker._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, "workers")

    def test_position_name(self):
        position_name = self.worker.position.name
        self.assertEqual(position_name, "Python Developer")

    def test_worker_str(self):
        expected = (f"{self.worker.username} "
                    f"({self.worker.first_name} "
                    f"{self.worker.last_name})")
        self.assertEqual(expected, str(self.worker))

    def test_get_absolute_url(self):
        expected = "/worker/1/"
        self.assertEqual(expected, self.worker.get_absolute_url())
