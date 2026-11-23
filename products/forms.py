
from pathlib import Path

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            "product_name",
            "brand",
            "category",
            "serial_number",
            "purchase_date",
            "warranty_months",
            "purchase_bill",
        ]

        widgets = {
            "product_name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. MacBook Air"
                }
            ),

            "brand": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Apple"
                }
            ),

            "category": forms.Select(),

            "serial_number": forms.TextInput(
                attrs={
                    "placeholder": "Enter product serial number"
                }
            ),

            "purchase_date": forms.DateInput(
                attrs={
                    "type": "date"
                },
                format="%Y-%m-%d"
            ),

            "warranty_months": forms.NumberInput(
                attrs={
                    "min": 0,
                    "max": 120,
                    "placeholder": "e.g. 12"
                }
            ),

            "purchase_bill": forms.ClearableFileInput(
                attrs={
                    "accept": ".pdf,.jpg,.jpeg,.png"
                }
            ),
        }

        labels = {
            "product_name": "Product Name",
            "brand": "Brand",
            "category": "Product Category",
            "serial_number": "Serial Number",
            "purchase_date": "Purchase Date",
            "warranty_months": "Warranty Duration (Months)",
            "purchase_bill": "Purchase Bill / Invoice",
        }

    # Validate purchase date
    def clean_purchase_date(self):
        purchase_date = self.cleaned_data["purchase_date"]

        if purchase_date > timezone.localdate():
            raise ValidationError(
                "Purchase date cannot be in the future."
            )

        return purchase_date

    # Validate warranty duration
    def clean_warranty_months(self):
        months = self.cleaned_data["warranty_months"]

        if months < 0:
            raise ValidationError(
                "Warranty duration cannot be negative."
            )

        if months > 120:
            raise ValidationError(
                "Warranty duration cannot exceed 120 months."
            )

        return months

    # Validate purchase bill
    def clean_purchase_bill(self):
        bill = self.cleaned_data.get("purchase_bill")

        if not bill:
            return bill

        allowed_extensions = {
            ".pdf",
            ".jpg",
            ".jpeg",
            ".png",
        }

        extension = Path(bill.name).suffix.lower()

        if extension not in allowed_extensions:
            raise ValidationError(
                "Only PDF, JPG, JPEG, and PNG files are allowed."
            )

        # Maximum file size: 5 MB
        max_size = 5 * 1024 * 1024

        if bill.size > max_size:
            raise ValidationError(
                "File size must be 5 MB or less."
            )

        # Check file signature
        position = bill.tell()
        bill.seek(0)
        header = bill.read(16)
        bill.seek(position)

        valid_pdf = (
            extension == ".pdf"
            and header.startswith(b"%PDF-")
        )

        valid_jpeg = (
            extension in {".jpg", ".jpeg"}
            and header.startswith(b"\xff\xd8\xff")
        )

        valid_png = (
            extension == ".png"
            and header.startswith(b"\x89PNG\r\n\x1a\n")
        )

        if not (
            valid_pdf
            or valid_jpeg
            or valid_png
        ):
            raise ValidationError(
                "The uploaded file does not match its format."
            )

        return bill
