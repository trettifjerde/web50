from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.FloatField(default=0)
    image = models.CharField(max_length=300, blank=True)
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Listing "{self.title}" ({"open" if self.status else "closed"})'

class Category(models.Model):
    name = models.CharField(max_length=50)
    listings = models.ManyToManyField(Listing, blank=True, related_name="categories")

    def __str__(self):
        return f"{self.name}"


class Bid(models.Model):
    price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid: {self.price} on {self.listing}"

class Comment(models.Model):
    text = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment: by {self.user} on {self.listing}"