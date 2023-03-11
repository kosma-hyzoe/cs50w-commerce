from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    starting_bid = models.FloatField()
    posted_datetime = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=30, null=True)
    image_url = models.CharField(max_length=2048, null=True)

    def __str__(self):
        return f"{self.title} @ {self.starting_bid}"


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    posted_datetime = models.DateTimeField(auto_now_add=True)
    current_price = models.FloatField()


class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    posted_datetime = models.DateTimeField(auto_now_add=True)


# todo choice
class Category(models.Model):
    pass

