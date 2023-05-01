from rest_framework import serializers
from .models import Images, UserImageRatingHistory, SelectionTypeChoices
from users.serializers import UserSerializer


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = "__all__"


class UserImageRatingHistorySerializer(serializers.ModelSerializer):
    """
    User Image Rating Serializer
    """
    user = UserSerializer(read_only=True)
    image = ImageSerializer(read_only=True)
    image_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = UserImageRatingHistory
        fields = ["id", "image", "user", "selection_type", "image_id"]

    def validate_image_id(self, image_id):
        """
        Validates image id
        If image id is valid, fetches the object and replaces the key with object
        Else If its Invalid, raises an Exception
        """
        image = Images.objects.filter(pk=image_id).first()
        if image is None:
            raise serializers.ValidationError("Invalid Image id %s." % image_id)

        return image

    def create(self, validated_data):
        image = validated_data.get("image_id")
        user = self.context['request'].user
        selection_type = validated_data.get("selection_type", SelectionTypeChoices.REJECTED)

        # As a image can be selected or rejected more than once,
        # we are updating the history with the latest selection the user has made for the image
        obj, created = UserImageRatingHistory.objects.update_or_create(
            user=user, image=image,
            defaults={"selection_type": selection_type},
        )

        return obj

