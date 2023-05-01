from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response

from project.json_rederer import ApiV3JSONRenderer
from .models import Images, UserImageRatingHistory, SelectionTypeChoices
from .serializers import ImageSerializer, UserImageRatingHistorySerializer


class ImagesViewSet(viewsets.ModelViewSet):
    """
    API endpoint to list all images.
    """
    queryset = Images.objects.all().order_by('-created_at')
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [ApiV3JSONRenderer]

    # caching the response for 10 minutes,
    # This is probably static and if it can be updated from DB,
    # so instead of caching forever,
    # caching it for some time gives us a chance to update the data automatically after 10 minutes
    @method_decorator(cache_page(10*60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserImageRatingHistoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint to save User Image Ratings and History.
    """
    queryset = UserImageRatingHistory.objects.all().order_by('-modified_at')
    serializer_class = UserImageRatingHistorySerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [ApiV3JSONRenderer]

    def get_queryset(self):
        return UserImageRatingHistory.objects.filter(user=self.request.user).order_by('-modified_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data

        # This Logic is to send related message for action taken by user
        # wrote the logic like this to avoid any DB queries to fetch username and image name,
        # as we already have them in serialized data
        user_name = data['user']['username']
        image_name = data['image']['name']
        selection_type = data['selection_type']

        message = f"{user_name}, you have rejected image {image_name}."
        if selection_type == SelectionTypeChoices.INTERESTED:
            message = f"{user_name}, you have selected image {image_name}."

        # Logic to check if user has rated all the images
        total_image_count = Images.objects.count()
        user_selected_image_count = self.get_queryset().count()

        if total_image_count == user_selected_image_count:
            message = f"{user_name}, you have rated all the images. Thank You!"

        headers = self.get_success_headers(serializer.data)
        return Response({"display_message": message, "data": serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)
