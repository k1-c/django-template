from django.conf.urls import url
from django.urls import include, path

from .views import CustomRegisterView, CustomConfirmEmailView

urlpatterns = [
    url(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        CustomConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path("", CustomRegisterView.as_view(), name='rest_register'),
    path("", include("rest_auth.registration.urls")),
]
