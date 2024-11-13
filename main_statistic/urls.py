from django.urls import path

from .views import PaymentListView, update_quantity

app_name = "main_statistic"

urlpatterns = [
    path("", PaymentListView.as_view(), name="main_statistic"),
    path("update-quantity/", update_quantity, name="update_quantity"),
]
