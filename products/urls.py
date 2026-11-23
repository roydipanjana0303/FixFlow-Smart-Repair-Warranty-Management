
from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.product_list,
        name="product_list"
    ),
    path(
        "add/",
        views.add_product,
        name="add_product"
    ),
    path(
        "<int:pk>/",
        views.product_detail,
        name="product_detail"
    ),
    path(
        "<int:pk>/bill/",
        views.download_purchase_bill,
        name="download_purchase_bill"
    ),
]
