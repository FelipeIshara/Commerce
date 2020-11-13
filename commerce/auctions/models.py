from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    listing_title = models.CharField(max_length=64)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=64)
    description = models.TextField()
    url_image = models.URLField()

    def __str__(self):
        return f"{self.listing_title}: has a starting bid of {starting_bid}"

class Bid(models.Model):
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids" )
    bid_value = models.DecimalField(max_digits=10, decimal_places=2)

class Comment(models.Model):
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment_text = models.TextField()



     
