from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from project.json_rederer import ApiV3JSONRenderer
from .models import Images, UserImageRatingHistory
from .serializers import ImageSerializer, UserImageRatingHistorySerializer


class ImagesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Images.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [ApiV3JSONRenderer]

    @method_decorator(cache_page(10*60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserImageRatingHistoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserImageRatingHistory.objects.all()
    serializer_class = UserImageRatingHistorySerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [ApiV3JSONRenderer]

    def get_queryset(self):
        return UserImageRatingHistory.objects.filter(user=self.request.user)

    @method_decorator(cache_page(5*60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(5*60))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
