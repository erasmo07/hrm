from django.urls import path
from django.contrib.auth import views as auth_views


from hrm.users import views


app_name = "users"

urlpatterns = [
    path("sing-in/", auth_views.LoginView.as_view(), name='signin'),
    path("sing-out/", auth_views.LogoutView.as_view(), name='signout'),
    path('sign-up/', views.SignUp.as_view(), name='signup'),
]
