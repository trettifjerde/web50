from django.contrib import admin

from .models import Listing, Bid, Comment, Category, User

admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(User)

