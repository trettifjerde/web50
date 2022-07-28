import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse

from auctions.models import User, Listing, Comment, Bid, Category
from auctions.forms import ListingForm, CommentForm


def index(request):
    listings = Listing.objects.filter(status=True).order_by('-created')
    return render(request, "auctions/index.html", {"title": "Active listings", "listings": listings})


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

def category(request, slug):
    try:
        cat = Category.objects.get(slug=slug)
        return render(request, "auctions/index.html", {"title": f"{cat.name} listings", "listings": Listing.objects.filter(category=cat, status=True)})
    except:
        pass
    return redirect("index")

@login_required
def new_listing(request):
    form = ListingForm({"user": request.user.id, "status": True, "starting_bid": 0})
    context = {"form": form, "action": "new"}
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save()
            return redirect('listing', listing_id=listing.id)
        else:
            context["errors"] = form.errors
    return render(request, 'auctions/listing_form.html', context)

def listing(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
        comments = listing.comments.all().order_by('created')
        context = {
            "listing": listing,
            "comments": comments,
        }
        if request.user.is_authenticated:
            context["commentForm"] = CommentForm()
            context["onwatchlist"] = request.user.watchlist.contains(listing)
        return render(request, "auctions/listing.html", context)
    except ObjectDoesNotExist:
        return renderMessagePage(request, {"text": "No such listing", "class": "error"})

@login_required()
def edit_listing(request, listing_id):
    #try:
        listing = Listing.objects.get(pk=listing_id)
        if listing.user == request.user and listing.status:
            form = ListingForm(instance=listing)
            if request.method == "POST":
                form = ListingForm(request.POST, request.FILES, instance=listing)
                if form.is_valid():
                    form.save()
                    return redirect("listing", listing_id=listing_id)  

            return render(request, "auctions/listing_form.html", {'form': form, 'action': 'edit', 'errors': form.errors})
        #else:
            #raise IntegrityError
    #except:
        #pass
        return redirect("listing", listing_id=listing_id)

@login_required
def close_listing(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.load(request)
        try:
            listing = Listing.objects.get(pk=data["listingId"])

            if request.user != listing.user: 
                raise Exception("not author")
            elif not listing.status:
                raise Exception("listing is already closed")
            elif listing.get_bids_length() == 0:
                raise Exception("no bids to agree to")

            listing.status = False
            listing.save()
            return JsonResponse({'redirect': f'{reverse("listing", args=(listing.id,))}'})
        except Exception as err:
            return JsonResponse({'msg': f'{err}'})
    return redirect("index")


@login_required
def delete_listing(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.load(request)
            listing = Listing.objects.get(pk=data['listingId'])
            if request.user == listing.user and listing.status:
                listing.delete()
                return JsonResponse({"redirect": reverse("profile")})
            else:
                raise Exception
        except Exception as err:
            return JsonResponse({"msg": f'{err}'})
    return redirect("index")

@login_required
def add_comment(request, listing_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            try:
                new_comment = form.save(commit=False)
                new_comment.user = request.user
                new_comment.listing = Listing.objects.get(pk=listing_id)
                new_comment.save()
                return redirect("listing", listing_id=listing_id)
            except: pass

    return renderMessagePage(request, {                    
            "text": "Error while adding a comment", 
            "class": "error",
            "redirect": reverse('listing', args=[listing_id])})

@login_required
def delete_comment(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.load(request)
            comment = Comment.objects.get(pk=data['commentId'])
            if comment.user == request.user:
                comment.delete()
                return JsonResponse({"redirect": ""})
            else:
                raise Exception('not author')
        except Exception as err:
            return JsonResponse({"msg": f'{err}'})
    return redirect("index")


@login_required
def watchlist_toggle(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.load(request)
            listing = Listing.objects.get(pk=data["listingId"])
            if request.user.is_authenticated and request.user != listing.user:
                if request.user.on_watchlist(listing):
                    request.user.watchlist.remove(listing)
                else:
                    request.user.watchlist.add(listing)
                return JsonResponse({"redirect": ""})
            else:
                raise Exception
        except Exception as err:
            return JsonResponse({"msg": f'{err}'})
    return redirect("index")

@login_required
def bid(request, listing_id):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(pk=listing_id)
            if listing.status:
                bid_price = float(request.POST["bid"])
                if bid_price > listing.get_current_bid_price():
                    bid = Bid(price=bid_price, user=request.user, listing=listing)
                    bid.save()
                else:
                    return renderMessagePage(request, {
                        "text": "Your bid is lesser than the current bid", 
                        "class": "error",
                        "redirect": reverse('listing', args=[listing_id])
                    })
            else:
                return renderMessagePage(request, {
                        "text": "This listing is closed", 
                        "class": "error",
                        "redirect": reverse('listing', args=[listing_id])
                    })
        except:
            pass
    return redirect("listing", listing_id=listing_id)

def userProfile(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        return render(request, "auctions/user.html", {"member": user})
    except ObjectDoesNotExist:
        return renderMessagePage(request, {"text": "No such user", "class": "error"})

def renderMessagePage(request, context):
    return render(request, "auctions/404.html", context)
        
@login_required
def profile(request):
    return redirect("user", user_id=request.user.id)

@login_required
def watchlist(request):
    if request.user.is_authenticated:
        return render(request, "auctions/index.html", {"title": "Watchlist", "listings": request.user.watchlist.all()})
    return redirect("index")

