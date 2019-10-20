from config.routers import router
from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView



urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('users/', include('hrm.users.urls', namespace='users')),
    path('', login_required(TemplateView.as_view(template_name='index.html')),
         name='home'),
    path('forget-password/',
         auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('forget-password/done/',
         auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('forget-password/<str:uidb64>/<str:token>/confirm/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('forget-password/complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
