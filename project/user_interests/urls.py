from django.urls import include, path
from rest_framework import routers
from .views import ImagesViewSet, UserImageRatingHistoryViewSet


router = routers.DefaultRouter()
router.register(r'images', ImagesViewSet, basename='images')
router.register(r'user_ratings', UserImageRatingHistoryViewSet, basename='user_ratings')

app_name = 'user_interests'
urlpatterns = [
    path('', include(router.urls)),
]
