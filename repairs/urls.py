
from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.ticket_list,
        name="ticket_list",
    ),
    path(
        "new/",
        views.create_ticket,
        name="create_ticket",
    ),
    path(
        "<int:pk>/",
        views.ticket_detail,
        name="ticket_detail",
    ),
]
