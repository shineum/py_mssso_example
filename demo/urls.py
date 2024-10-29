from . import views
from django.urls import path

urlpatterns = [
    path("", views.index),
    path("logout/", views.logout_view),
    path("sso_login/", views.sso_login),
    path("sso_login_callback/", views.sso_login_callback),
]
