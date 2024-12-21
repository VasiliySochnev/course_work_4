from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from config import settings
from mailing_service import views
from mailing_service.views import homeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", homeView.as_view(), name="home"),
    path("", include("mailing_service.urls", namespace="mailing")),
    path("users/", include("auth_users.urls", namespace="users")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)