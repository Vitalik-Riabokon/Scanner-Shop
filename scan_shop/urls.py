# from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("scan/", include("scanner_barcode.urls", namespace="scanner_barcode")),
        path("", include("main_statistic.urls", namespace="main_statistic")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # + debug_toolbar_urls()
)
