from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls.static import static
from auth_users.apps import AuthUsersConfig
from auth_users.views import (
    UserCreateView,
    UserDeleteView,
    UserDetailView,
    UserListView,
    UserUpdateView,
    email_verification, PasswordRecoveryView, user_logout,
)

app_name = AuthUsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="auth_users/login.html"), name="login"),
    path("logout/", user_logout, name="logout"),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="reset_password"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("detail/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="user_update"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="user_delete"),
    path("password-recovery/", PasswordRecoveryView.as_view(), name="password_recovery"),
]
