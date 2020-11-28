from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
class User(AbstractUser):
    pass



class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=64, blank=True)
    description = models.TextField(blank=True)
    url_image = models.URLField(blank=True)
    active = models.BooleanField(default=True, blank=False)
    last_bid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.title} listed by {self.owner}"



class Bid(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids" )
    bid_value = models.DecimalField(max_digits=10, decimal_places=2)

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(blank=False)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    watchlist = models.ManyToManyField(Listing, related_name="interessed_users", blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print("Creating profile")
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print("SAVING profile")
    instance.profile.save()