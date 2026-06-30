from django.db import models


class SocialPlatform(models.TextChoices):

    FACEBOOK = "facebook", "Facebook"

    INSTAGRAM = "instagram", "Instagram"

    X = "x", "X"

    