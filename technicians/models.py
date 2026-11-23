
from django.db import models
from django.conf import settings


class Technician(models.Model):

    SPECIALIZATION_CHOICES = [
        ("laptop", "Laptop"),
        ("mobile", "Mobile Phone"),
        ("tv", "Television"),
        ("ac", "Air Conditioner"),
        ("refrigerator", "Refrigerator"),
        ("washing_machine", "Washing Machine"),
        ("other", "Other"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="technician_profile"
    )

    specialization = models.CharField(
        max_length=30,
        choices=SPECIALIZATION_CHOICES
    )

    experience_years = models.PositiveIntegerField(
        default=0
    )

    is_available = models.BooleanField(default=True)

    max_active_tickets = models.PositiveIntegerField(
        default=5
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username
