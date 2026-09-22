from django.test import TestCase
from django.urls import reverse

from .models import Fish


class AquariumTests(TestCase):
    def test_starter_fish_exist(self):
        self.assertEqual(Fish.objects.count(), 3)

    def test_index_renders(self):
        res = self.client.get(reverse("tank:index"))
        self.assertContains(res, "Pocket Aquarium")
        self.assertContains(res, "Coral")

    def test_add_fish(self):
        res = self.client.post(
            reverse("tank:index"),
            {"name": "Finn", "color": "#3366ff", "size": 80, "speed": 14},
        )
        fish = Fish.objects.get(name="Finn")
        self.assertRedirects(res, f"{reverse('tank:index')}?new={fish.pk}")
        self.assertTrue(16 <= fish.depth <= 76)

    def test_bad_colour_rejected(self):
        res = self.client.post(
            reverse("tank:index"),
            {"name": "Oops", "color": "red", "size": 80, "speed": 14},
        )
        self.assertEqual(res.status_code, 200)
        self.assertFalse(Fish.objects.filter(name="Oops").exists())

    def test_feeding_grows_fish(self):
        fish = Fish.objects.first()
        before = fish.display_size
        res = self.client.post(reverse("tank:feed", args=[fish.pk]))
        self.assertEqual(res.json()["meals"], 1)
        self.assertEqual(res.json()["size"], before + 3)

    def test_release_fish(self):
        fish = Fish.objects.first()
        self.client.post(reverse("tank:release", args=[fish.pk]))
        self.assertFalse(Fish.objects.filter(pk=fish.pk).exists())

    def test_feed_requires_post(self):
        fish = Fish.objects.first()
        self.assertEqual(self.client.get(reverse("tank:feed", args=[fish.pk])).status_code, 405)
