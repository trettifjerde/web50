from django.contrib import admin

from .models import Listing, Bid, Comment, Category, User

class ListingInline(admin.StackedInline):
    model = Listing
    extra = 0

class BidInline(admin.TabularInline):
    model = Bid
    extra = 0

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0

class UserAdmin(admin.ModelAdmin):
    exclude = ('email', 'last_login', 'date_joined')
    inlines = [ListingInline, CommentInline, BidInline]

class ListingAdmin(admin.ModelAdmin):
    inlines = [BidInline, CommentInline]
    filter_horizontal = ('category', )

admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(User, UserAdmin)

