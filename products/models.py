
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class Product(models.Model):

    CATEGORY_CHOICES = [
        ("laptop", "Laptop"),
        ("mobile", "Mobile Phone"),
        ("tv", "Television"),
        ("ac", "Air Conditioner"),
        ("refrigerator", "Refrigerator"),
        ("washing_machine", "Washing Machine"),
        ("other", "Other"),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products"
    )

    product_name = models.CharField(max_length=150)

    brand = models.CharField(max_length=100)

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    serial_number = models.CharField(
        max_length=100,
        unique=True
    )

    purchase_date = models.DateField()

    warranty_months = models.PositiveIntegerField(
        default=12
    )

    purchase_bill = models.FileField(
        upload_to="purchase_bills/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    @property
    def warranty_expiry(self):
        # Calendar-month calculation
        from calendar import monthrange

        total_months = (
            self.purchase_date.year * 12
            + self.purchase_date.month - 1
            + self.warranty_months
        )

        year, month_index = divmod(total_months, 12)
        month = month_index + 1

        day = min(
            self.purchase_date.day,
            monthrange(year, month)[1]
        )

        return self.purchase_date.replace(
            year=year,
            month=month,
            day=day
        )

    @property
    def is_under_warranty(self):
        today = timezone.localdate()

        return (
            self.purchase_date <= today
            and today <= self.warranty_expiry
        )

    def __str__(self):
        return f"{self.brand} {self.product_name}"
