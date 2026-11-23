
from django.urls import path
from . import views

app_name = "technicians"

urlpatterns = [
    path(
        "",
        views.technician_dashboard,
        name="dashboard",
    ),
    path(
        "repairs/<int:pk>/",
        views.technician_ticket_detail,
        name="ticket_detail",
    ),
]
