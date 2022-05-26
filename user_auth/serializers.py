from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key if token else ""

    class Meta:
        model = User
        fields = ["pk", "username", "first_name", "last_name", "email", "token"]
