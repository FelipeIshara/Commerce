from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import CreateListingForm, PlaceBidForm
from decimal import Decimal
from django.db.models import Max


from .models import User, Listing, Bid


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html",{
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            starting_price = form.cleaned_data["starting_price"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            url_image = form.cleaned_data["url_image"]
            
            instListing = Listing(
                owner_id= request.user, 
                title=title, 
                starting_price=starting_price, 
                category=category,
                url_image = url_image
            )
            instListing.save()
            return HttpResponseRedirect(reverse("listing", args=(instListing.pk,)))


    form = CreateListingForm()
    return render(request, "auctions/createlisting.html",{
        "form": form
    })

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    already_on_watchlist = request.user.profile.watchlist.filter(id=listing_id)
    form = PlaceBidForm()
    #Query the biggest bid, if there is no bids return null
    biggest_bid = listing.bids.all().order_by('-bid_value').first()
    if not biggest_bid:
        price = listing.starting_price
    else:
        price = biggest_bid.bid_value
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "already_on_watchlist": already_on_watchlist,
        "PlaceBidForm": form,
        "price": price
    })

def watchlist(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        listing_id = int(request.POST["listing_id"])
        listing = Listing.objects.get(pk=listing_id)
        user.profile.watchlist.add(listing)
        return HttpResponseRedirect(reverse("watchlist"))
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.profile.watchlist,
        
    })
def watchlist_delete(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        listing_id = int(request.POST["listing_id"])
        listing = Listing.objects.get(pk=listing_id)
        watchlist_item = request.user.profile.watchlist.get(id=listing_id)
        user.profile.watchlist.remove(listing)
        return HttpResponseRedirect(reverse("watchlist"))

def bid(request):
    #Convert data to decimal
    if request.method == "POST":
        bid = round(Decimal(request.POST["bid_value"].replace(',','.')), 2)
        listing_id = int(request.POST["listing_id"])
        listing = Listing.objects.get(pk=listing_id)
        if bid < listing.starting_price:
            return HttpResponse("Your bid must be greater than or equal to the starting bid")
        biggest_bid = listing.bids.all().order_by('-bid_value').first()
        if bid < biggest_bid.bid_value:
            return HttpResponse("Your bid must be greater than the last bid")
        bid_inst = Bid(
        owner = request.user,
        listing_id = listing,
        bid_value = bid
        )
        bid_inst.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))