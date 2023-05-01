from django.db import models
from users.models import BaseModel, User
# Create your models here.


class Images(BaseModel):
    """
    Model to save Images
    """
    name = models.CharField(max_length=100)
    image_url = models.URLField(max_length=256)


class SelectionTypeChoices(models.TextChoices):
    """
    Choices for Selection Type for a image by a user
    """
    INTERESTED = "interested"
    REJECTED = "rejected"


class UserImageRatingHistory(BaseModel):
    """
    Model to save user image ratings and history
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_image_history")
    image = models.ForeignKey(Images, on_delete=models.CASCADE, related_name="image_history")
    selection_type = models.CharField(max_length=25, choices=SelectionTypeChoices.choices,
                                      default=SelectionTypeChoices.INTERESTED)
