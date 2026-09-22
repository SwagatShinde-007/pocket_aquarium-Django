from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Fish(models.Model):
    name = models.CharField(max_length=24)
    color = models.CharField(max_length=7, default="#ff6f59")
    size = models.PositiveSmallIntegerField(
        default=110, validators=[MinValueValidator(50), MaxValueValidator(200)]
    )
    # seconds the fish takes to swim from one side of the tank to the other
    speed = models.PositiveSmallIntegerField(
        default=16, validators=[MinValueValidator(6), MaxValueValidator(40)]
    )
    depth = models.PositiveSmallIntegerField(default=40)  # % from the top
    meals = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "fish"

    def __str__(self):
        return self.name

    @property
    def display_size(self):
        """Fish grow a little with every meal (up to 25 meals)."""
        return self.size + min(self.meals, 25) * 3

    @property
    def level(self):
        if self.meals >= 20:
            return "Legend"
        if self.meals >= 10:
            return "Chunky"
        if self.meals >= 3:
            return "Growing"
        return "Tiny"

    @property
    def delay(self):
        """Negative delay so fish start at different spots along the tank."""
        return -((self.pk or 1) * 5 % (self.speed * 2))
