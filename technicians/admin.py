
from django.contrib import admin
from .models import Technician


@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "specialization",
        "experience_years",
        "is_available",
        "max_active_tickets",
    )

    list_filter = ("specialization", "is_available")
