
from django import forms


class RepairProgressForm(forms.Form):
    STATUS_CHOICES = [
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "tech-input"}),
    )

    message = forms.CharField(
        min_length=5,
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                "class": "tech-input",
                "rows": 4,
                "placeholder": "Describe the repair work performed...",
            }
        ),
        label="Repair Update",
    )
