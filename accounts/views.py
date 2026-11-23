
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .forms import CustomerRegistrationForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                user = form.save()

            login(request, user)
            messages.success(
                request,
                "Welcome to FixFlow! Your account is ready."
            )
            return redirect("dashboard")
    else:
        form = CustomerRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(
                request,
                "You have logged in successfully."
            )
            return redirect("dashboard")
    else:
        form = AuthenticationForm(request)

    return render(
        request,
        "accounts/login.html",
        {"form": form}
    )


@login_required
@require_POST
def logout_view(request):
    logout(request)
    messages.success(
        request,
        "You have been logged out successfully."
    )
    return redirect("landing")
