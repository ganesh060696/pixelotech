from rest_framework import serializers
from .models import Images, UserImageRatingHistory, SelectionTypeChoices
from users.models import User
from users.serializers import UserSerializer


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = "__all__"


class UserImageRatingHistorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    image = ImageSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=True)
    image_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = UserImageRatingHistory
        fields = ["id", "image", "user", "selection_type", "user_id", "image_id"]

    def validate_image_id(self, image_id):
        image = Images.objects.filter(pk=image_id).first()
        if image is None:
            raise serializers.ValidationError("Invalid Image id %s." % image_id)

        return image

    def validate_user_id(self, user_id):
        user = User.objects.filter(pk=user_id).first()
        if user is None:
            raise serializers.ValidationError("Invalid Image id %s." % user_id)

        return user

    def create(self, validated_data):
        image = validated_data.get("image_id")
        user = validated_data.get("user_id")
        selection_type = validated_data.get("selection_type", SelectionTypeChoices.REJECTED)

        # As a image can be selected or rejected more than once,
        # we are updating the history with the latest selection the user has made for the image
        obj, created = UserImageRatingHistory.objects.update_or_create(
            user=user, image=image,
            defaults={"selection_type": selection_type},
        )

        # obj = UserImageRatingHistory.objects.create(
        #     user=user, image=image, selection_type=selection_type
        # )

        return obj

