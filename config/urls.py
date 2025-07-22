from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

handler403 = "config.views.custom_permission_denied"
handler404 = "config.views.custom_page_not_found"
handler500 = "config.views.custom_error_handler"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    path("ads/", include("ads.urls", namespace="ads")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
