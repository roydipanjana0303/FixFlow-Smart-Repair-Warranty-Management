
from django.db import models
from django.conf import settings


class RepairTicket(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("assigned", "Assigned"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    WARRANTY_CHOICES = [
        ("pending", "Pending Review"),
        ("eligible", "Eligible"),
        ("expired", "Expired"),
        ("not_covered", "Not Covered"),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="repair_tickets"
    )

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="repair_tickets"
    )

    issue_description = models.TextField()

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    warranty_status = models.CharField(
        max_length=20,
        choices=WARRANTY_CHOICES,
        default="pending"
    )

    assigned_technician = models.ForeignKey(
        "technicians.Technician",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Ticket #{self.id} - {self.product}"


class RepairUpdate(models.Model):

    ticket = models.ForeignKey(
        RepairTicket,
        on_delete=models.CASCADE,
        related_name="updates"
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Update for Ticket #{self.ticket_id}"
