
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django Admin
    path(
        "admin/",
        admin.site.urls,
    ),

    # Customer Accounts
    path(
        "accounts/",
        include("accounts.urls"),
    ),

    # Product and Warranty Management
    path(
        "products/",
        include("products.urls"),
    ),

    # Repair Ticket Management
    path(
        "repairs/",
        include("repairs.urls"),
    ),

    # Technician Workspace
    path(
        "technician/",
        include("technicians.urls"),
    ),

    # Phase 7 REST APIs
    path(
        "api/",
        include("api.urls"),
    ),

    # Homepage and Customer Dashboard
    path(
        "",
        include("dashboard.urls"),
    ),
]

# Serve uploaded files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
