from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/close", views.close_listing, name="close_listing"),
    path("listing/<int:listing_id>/edit", views.edit_listing, name="edit_listing"),
    path("listing/<int:listing_id>/delete", views.delete_listing, name="delete_listing"),
    path("listing/<int:listing_id>/bid", views.bid, name="bid"),
    path("users/<int:user_id>", views.userProfile, name="user")
]
