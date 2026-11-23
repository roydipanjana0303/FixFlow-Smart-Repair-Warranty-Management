
from django.urls import path

from .views import (
    AdminAnalyticsAPI,
    ProductListAPI,
    RepairTicketListAPI,
    TechnicianTicketsAPI,
)

urlpatterns = [
    path(
        "products/",
        ProductListAPI.as_view(),
        name="api_products",
    ),

    path(
        "repairs/",
        RepairTicketListAPI.as_view(),
        name="api_repairs",
    ),

    path(
        "technician/repairs/",
        TechnicianTicketsAPI.as_view(),
        name="api_technician_repairs",
    ),

    path(
        "admin/analytics/",
        AdminAnalyticsAPI.as_view(),
        name="api_admin_analytics",
    ),
]
