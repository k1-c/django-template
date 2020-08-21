from rest_framework import serializers
from rest_auth.serializers import PasswordResetSerializer
from rest_auth.registration.serializers import RegisterSerializer
from .models import User
from django.conf import settings


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)

    def get_cleaned_data(self):

        return {
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
        }

    # Userモデルにプロパティが増えた場合はここでオーバーライドする.
    # def custom_signup(self, request, user):


class CustomPasswordResetSerializer(PasswordResetSerializer):
    def validate_email(self, value):
        super().validate_email(value)
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('そのメールアドレスは登録されていません。')
        return value

    def get_email_options(self):
        email_context = {
            'front_password_reset_url': settings.FRONT_HOST + '/reset-password/confirm'
        }

        return {
            'subject_template_name': 'auth/email/password_reset_subject.txt',
            'email_template_name': 'auth/email/password_reset_body.txt',
            'extra_email_context': email_context
        }


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "email"]
        read_only_fields = ["pk", "email"]
