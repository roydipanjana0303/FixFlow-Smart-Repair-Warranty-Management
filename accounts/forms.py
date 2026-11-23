
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomerProfile


class CustomerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 2}),
        required=False
    )

    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "username",
            "email", "phone", "address",
            "password1", "password2"
        ]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            CustomerProfile.objects.create(
                user=user,
                phone=self.cleaned_data["phone"],
                address=self.cleaned_data["address"],
                role="customer"
            )

        return user
