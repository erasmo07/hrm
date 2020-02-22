from config.routers import router
from django.conf import settings
from django.urls import include, path, re_path, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from rest_framework.authtoken.views import ObtainAuthToken
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('', RedirectView.as_view(url=reverse_lazy('api-root'),permanent=False)),

    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include('rest_framework.urls', namespace='rest_framework')),

    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
