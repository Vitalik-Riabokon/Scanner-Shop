from django.urls import path

from .views import confirm_purchase, scan_barcode

app_name = "scanner_barcode"

urlpatterns = [
    path("", scan_barcode, name="scan_barcode"),
    path(
        "confirm-purchase/", confirm_purchase, name="confirm_purchase"
    ),  # Цей шлях має бути
]
