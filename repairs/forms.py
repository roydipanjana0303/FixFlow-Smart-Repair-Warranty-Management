
from django import forms
from products.models import Product
from .models import RepairTicket


class RepairTicketForm(forms.ModelForm):
    class Meta:
        model = RepairTicket
        fields = [
            "product",
            "issue_description",
            "priority",
        ]

        widgets = {
            "product": forms.Select(),
            "issue_description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": (
                        "Describe the issue with your device..."
                    ),
                }
            ),
            "priority": forms.Select(),
        }

        labels = {
            "product": "Select Your Product",
            "issue_description": "Describe the Problem",
            "priority": "Repair Priority",
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["product"].queryset = (
            Product.objects.filter(
                customer=user
            ).order_by("-created_at")
            if user and user.is_authenticated
            else Product.objects.none()
        )

        self.fields["product"].empty_label = (
            "Choose a registered product"
        )

        self.fields["issue_description"].min_length = 10

    def clean_issue_description(self):
        description = self.cleaned_data[
            "issue_description"
        ].strip()

        if len(description) < 10:
            raise forms.ValidationError(
                "Please describe the issue in at least 10 characters."
            )

        return description
