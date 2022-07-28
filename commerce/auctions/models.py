from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.db import models


class User(AbstractUser):
    def on_watchlist(self, listing):
        return self.watchlist.contains(listing)

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50)
    color = models.CharField(max_length=7)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    class Meta:
        ordering = ['-created']

    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.FloatField(default=0)
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to="listings/", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, blank=True, related_name="listings")
    watchlist = models.ManyToManyField(User, related_name="watchlist", blank=True)

    def __str__(self):
        return f'Listing "{self.title}" ({"open" if self.status else "closed"})'
    
    def get_current_bid_price(self):
        return self.bids.first().price if self.get_bids_length() else self.starting_bid

    def get_current_bid_user(self):
        return self.bids.first().user
    
    def get_bids_length(self):
        return len(self.bids.all())

    def get_winner(self):
        return self.get_current_bid_user() if not self.status else None


class Bid(models.Model):

    class Meta:
        ordering = ['-price']

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