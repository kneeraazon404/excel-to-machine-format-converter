from django.urls import path


from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
from course import views as user_views

urlpatterns = [
    path("", user_views.dashboard, name="dashboard"),
    path("create/", user_views.create_view, name="create"),
    path("register/", user_views.register, name="register"),
    path("profile/", user_views.profile, name="profile"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="account/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="account/logout.html"),
        name="logout",
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="account/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "add_market_id/",
        user_views.add_market_id,
        name="add_market_id",
    ),
    path(
        "add_store_number/",
        user_views.add_store_number,
        name="add_store_number",
    ),
    path(
        "add_terminal_id/",
        user_views.add_terminal_id,
        name="add_terminal_id",
    ),
    path(
        "add_brand_name/",
        user_views.add_brand_name,
        name="add_brand_name",
    ),
    path("store-create/", user_views.create_view, name="store-create"),
    path("store-update/<id>/", user_views.update_view, name="store-update"),
    path("store-delete/<id>/", user_views.delete_view, name="store-delete"),
    path("user-delete/<id>/", user_views.delete_user_view, name="user-delete"),
    path("user_update/<id>/", user_views.user_update_view, name="user-update"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
