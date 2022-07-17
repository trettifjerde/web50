from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from .models import User, Listing, Comment, Bid, Category


def index(request):
    listings = Listing.objects.filter(status=True).order_by('-created')
    return render(request, "auctions/index.html", {"listings": listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect("index")
    else:
        return render(request, "auctions/register.html")

def categories(request):
    pass

def listing(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
        comments = listing.comments.all().order_by('created')
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments
            })
    except ObjectDoesNotExist:
        return render(request, "auctions/404.html", {"message": {"text": "No such listing", "class": "error"}})

def userProfile(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        return render(request, "auctions/user.html", {"user": user})
    except ObjectDoesNotExist:
        return render(request, "auctions/404.html", {"message": {"text": "No such user", "class": "error"}})
        
@login_required
def profile(request):
    return redirect("index")

@login_required
def watchlist(request):
    pass

@login_required
def new_listing(request):
    pass

