
from django.db import models
from django.conf import settings


class CustomerProfile(models.Model):

    ROLE_CHOICES = [
        ("customer", "Customer"),
        ("technician", "Technician"),
        ("admin", "Admin"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    address = models.TextField(blank=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="customer"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"
