import uuid
from django.db import models, transaction
from auth.models import User

optional = {
    "null": True,
    "blank": True,
}


class AppConfig(models.Model):
    """AppConfigモデル
    アプリケーション全体の設定値モデル
    """
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "App Config"

    def save(self, *args, **kwargs):
        self.pk = 1
        super(AppConfig, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class UserProfile(models.Model):
    """UserProfileモデル
    ユーザーのコアデータ。auth-userと一対一で紐づく
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    username = models.CharField(max_length=32)
    birthday = models.DateField()
    phone_number = models.CharField(max_length=11, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.username)

    class Meta:
        model = models
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
