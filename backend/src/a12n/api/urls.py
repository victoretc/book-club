from django.conf import settings
from django.urls import path

from a12n.api import views


app_name = "a12n"

urlpatterns = [
    path("token/", views.TokenObtainPairView.as_view(), name="auth_obtain_pair"),
    path("token/refresh/", views.TokenRefreshView.as_view(), name="auth_refresh"),
    path("logout/", views.TokenBlacklistView.as_view(), name="auth_logout"),
    path("code/", views.RequestCodeView.as_view(), name="auth_request_code"),
    path("code/verify/", views.VerifyCodeView.as_view(), name="auth_verify_code"),
]

if settings.DEBUG:
    urlpatterns += [
        path("code/retrieve/", views.RetrieveCodeView.as_view(), name="auth_retrieve_code"),
    ]
