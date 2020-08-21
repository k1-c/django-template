import urllib.parse

from allauth.account import app_settings as allauth_settings
from allauth.account.models import EmailConfirmationHMAC
from allauth.account.utils import complete_signup
from allauth.account.views import ConfirmEmailView
from django.db import transaction
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_auth.app_settings import create_token
from rest_auth.registration.serializers import VerifyEmailSerializer
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from rest_auth.registration.views import RegisterView


class CustomRegisterView(RegisterView):
    queryset = User.objects.all()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(request)

        create_token(self.token_model, user, serializer)

        request.data["user"] = user.pk

        complete_signup(self.request._request, user, allauth_settings.EMAIL_VERIFICATION, None)

        headers = self.get_success_headers(serializer.data)
        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)


def get_optional_params(confirmation: EmailConfirmationHMAC):
    return {}


class CustomConfirmEmailView(APIView, ConfirmEmailView):
    """ ユーザー登録の email verification. """

    permission_classes = (AllowAny,)
    allowed_methods = ("GET", "OPTIONS", "HEAD")

    def get_serializer(*args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=kwargs)
        try:
            serializer.is_valid(raise_exception=True)
            self.kwargs["key"] = serializer.validated_data["key"]
            confirmation = self.get_object()
            confirmation.confirm(self.request)
            params = {"detail": _("ok"), "status": status.HTTP_200_OK}
            params.update(get_optional_params(confirmation))

        except ValidationError as e:
            params = {"detail": _("invalid"), "status": e.status_code}
        except Http404:
            params = {"detail": _("invalid"), "status": status.HTTP_404_NOT_FOUND}

        # Front サーバーへリダイレクト.
        url = settings.FRONT_HOST + "/signup/done"
        # クエリパラメータに認証結果を付与
        url = "{}?{}".format(url, urllib.parse.urlencode(params))
        return HttpResponseRedirect(redirect_to=url)
