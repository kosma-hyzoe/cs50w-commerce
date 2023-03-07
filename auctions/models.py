from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    starting_bid = models.FloatField()
    date_posted = models.DateField(default=datetime.now())
    current_bid = models.FloatField(null=True)
    category = models.CharField(max_length=30, null=True)
    image_url = models.CharField(max_length=2048, null=True)

    def __str__(self):
        return f"{self.title} @ {self.starting_bid}"


class Bid:
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    # starting_price = models.FloatField()
    current_price = models.FloatField()


class Comment:
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()


