from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, reverse

from auctions.models import User, Listing, Comment, Bid, Category
from auctions.forms import ListingForm


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
            return redirect('index')
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
    return render(request, 'auctions/categories.html', {'categories': Category.objects.all()})

@login_required
def new_listing(request):
    form = ListingForm({"user": request.user.id, "status": True})
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save()
            return redirect('listing', listing_id=listing.id)
    return render(request, 'auctions/listing_form.html', {"form": form, "action": "new"})

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

@login_required()
def edit_listing(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
        if listing.user == request.user:
            form = ListingForm(instance=listing)
            if request.method == "POST":
                form = ListingForm(request.POST, instance=listing)
                print(form.is_bound)
                if form.is_valid():
                    form.save()
                    return redirect("listing", listing_id=listing_id)    
            return render(request, "auctions/listing_form.html", {'form': form, "action": "edit"})
        else:
            raise IntegrityError
    except:
        pass
    return redirect("listing", listing_id=listing_id)

@login_required
def close_listing(request, listing_id):
    pass

@login_required
def delete_listing(request, listing_id):
    pass

@login_required
def bid(request, listing_id):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(pk=listing_id)
            bid_price = float(request.POST["bid"])
            if bid_price > listing.get_current_bid_price():
                bid = Bid(price=bid_price, user=request.user, listing=listing)
                bid.save()
            else:
                return renderMessagePage(request, {
                    "message": {
                        "text": "Your bid is lesser than the current bid", 
                        "class": "error"},
                    "redirect": reverse('listing', args=[listing_id])
                    })
        except:
            pass
    return redirect("listing", listing_id=listing_id)

def userProfile(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        return render(request, "auctions/user.html", {"user": user})
    except ObjectDoesNotExist:
        return renderMessagePage(request, {"message": {"text": "No such user", "class": "error"}})

def renderMessagePage(request, context):
    return render(request, "auctions/404.html", context)
        
@login_required
def profile(request):
    return redirect("user", user_id=request.user.id)

@login_required
def watchlist(request):
    pass

