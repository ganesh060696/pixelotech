from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'is_profile_complete', 'token',
                  'created_at', 'modified_at']

    def get_token(self, user):
        return user.auth_token.key

    def update(self, instance, validated_data):
        username = validated_data.get("username")

        if username:
            instance.is_profile_complete = True

        instance.username = username
        instance.save()

        return instance
