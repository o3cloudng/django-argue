from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/clearcache/", include("clearcache.urls")),
    path("admin/", admin.site.urls),
    path("api/user/", include("accounts.urls")),
    path("api-auth/", include("rest_framework.urls")),
    # path("api/roles/", include("app.urls")),
    path("api/settings/", include("data_settings.urls")),
    path("api/aircraft-temp-manager/", include("aircraft_template_manager.urls")),
    path("api/occurrence-meta-data/", include("occurrence_report.urls")),
    # Audit Trail Path
    # path("dj-audit/", include('dj_audit.urls')),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "helpers.views.error_404"
handler400 = "helpers.views.error_400"
handler500 = "helpers.views.error_500"
