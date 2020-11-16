from django.contrib import admin
from .models import User, Comment, Listing, Bid, Profile
# Register your models here.

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Profile)