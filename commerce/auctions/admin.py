from django.contrib import admin

from .models import Listing, Bid, Comment, Category, User

class BidInline(admin.StackedInline):
    model = Bid
    extra = 1

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1

class CategoriesInline(admin.StackedInline):
    model = Category.listings.through
    extra = 1

class ListingAdmin(admin.ModelAdmin):
    inlines = [CategoriesInline, BidInline, CommentInline]

admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(User)

