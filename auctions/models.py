from collections import namedtuple

from django.contrib.auth.models import AbstractUser
from django.db import models

CategoryChoice = namedtuple("CategoryChoice", ['abbreviation', 'full_name'])


class User(AbstractUser):
    pass


class Listing(models.Model):
    ELECTRONICS = 'EL'
    CLOTHING = 'CL'
    HOME_AND_GARDEN = 'HG'
    HEALTH_AND_BEAUTY = 'HB'
    SPORTS_AND_OUTDOORS = 'SO'
    TOYS_AND_GAMES = 'TG'
    BOOKS_AND_MEDIA = 'BM'
    AUTOMOTIVE = 'AM'
    PET_SUPPLIES = 'PS'
    FOOD_AND_BEVERAGES = 'FB'
    OTHER = 'OT'
    CATEGORY_CHOICES = [
        CategoryChoice(OTHER, 'Other'),
        CategoryChoice(ELECTRONICS, 'Electronics'),
        CategoryChoice(CLOTHING, 'Clothing'),
        CategoryChoice(HOME_AND_GARDEN, 'Home & Garden'),
        CategoryChoice(HEALTH_AND_BEAUTY, 'Health & Beauty'),
        CategoryChoice(SPORTS_AND_OUTDOORS, 'Sports & Outdoors'),
        CategoryChoice(TOYS_AND_GAMES, 'Toys & Games'),
        CategoryChoice(BOOKS_AND_MEDIA, 'Books & Media'),
        CategoryChoice(AUTOMOTIVE, 'Automotive'),
        CategoryChoice(PET_SUPPLIES, 'Pet Supplies'),
        CategoryChoice(FOOD_AND_BEVERAGES, 'Food & Beverages'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="buyers")
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=5000)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=10)
    current_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    posted_datetime = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, null=True)
    image_url = models.CharField(max_length=2048, null=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.current_price == 0:
            self.current_price = self.starting_bid
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.user.username}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listings = models.ManyToManyField(Listing)


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    posted_datetime = models.DateTimeField(auto_now_add=True)
    value = models.DecimalField(decimal_places=2, default=0, max_digits=10)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    posted_datetime = models.DateTimeField(auto_now_add=True)
