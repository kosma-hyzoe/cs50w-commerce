from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from . import forms
from .models import User, Listing, Bid, CategoryChoice, Comment, Watchlist


def index(request):
    return render(request, "auctions/index.html",
                  {"listings": Listing.objects.filter(buyer__isnull=True).order_by('-posted_datetime')})


def archive(request):
    return render(request, "auctions/archive.html",
                  {"listings": Listing.objects.filter(buyer__isnull=False).order_by('-posted_datetime')})


@login_required(login_url="/login")
def create(request):
    if request.method == "POST":
        form = forms.CreateNewListing(request.POST)
        if form.is_valid():
            listing = Listing(
                user=request.user,
                title=form.cleaned_data.get("title"),
                description=form.cleaned_data.get("description"),
                starting_bid=form.cleaned_data.get("starting_bid"),
                image_url=form.cleaned_data.get("image_link"),
                category=form.cleaned_data.get("category")
            )
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = forms.CreateNewListing()
        return render(request, "auctions/create.html", {"form": form})


@login_required(login_url="/login")
def listing_view(request, listing_id):
    message = None
    # todo move somewhere
    try:
        watchlist = Watchlist.objects.get(user=request.user)
    except Watchlist.DoesNotExist:
        watchlist = Watchlist(user=request.user)
        watchlist.save()

    try:
        listing = Listing.objects.get(id=listing_id)
        on_watchlist = watchlist.listings.filter(id=listing.id).exists()
        highest_bid = Bid.objects.filter(listing=listing).order_by("-value").first()
    except Bid.DoesNotExist:
        highest_bid = None
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")

    if request.method == "POST":
        # check if the 'your bid' form was submitted
        if 'value' in request.POST:
            your_bid_form = forms.YourBid(request.POST)
            if your_bid_form.is_valid():
                your_bid_value = your_bid_form.cleaned_data.get("value")
                # check if bid value is higher than the highest/starting bid
                if your_bid_value < listing.starting_bid or highest_bid and your_bid_value < highest_bid.value:
                    message = "The value of your bid is invalid! Please try again."
                else:
                    highest_bid = Bid(user=request.user, listing=listing, value=your_bid_value)
                    highest_bid.save()
                    message = f"You just bid this auction for ${your_bid_value:.2f}."
            else:
                message = "Invalid bid value"
        # check if the comment form was submitted
        if 'content' in request.POST:
            comment_form = forms.CommentForm(request.POST)
            if comment_form.is_valid():
                comment_content = comment_form.cleaned_data.get("content")
                message = "Comment posted."
                comment = Comment(content=comment_content, user=request.user, listing=listing)
                comment.save()
            else:
                message = "Invalid comment content."

    if "sell" in request.POST:
        buyer = highest_bid.user
        listing.buyer = buyer
        listing.save()
        message = "You just sold this item!"
    elif "watchlist" in request.POST:

        if on_watchlist:
            on_watchlist = False
            watchlist.listings.remove(listing)
        else:
            watchlist.listings.add(listing)
            on_watchlist = True

    your_bid_form = forms.YourBid()
    comment_form = forms.CommentForm()

    comments = Comment.objects.filter(listing=listing).order_by("-posted_datetime")
    return render(request, "auctions/listing.html",
                  {"listing": listing, "highest_bid": highest_bid,
                   "your_bid_form": your_bid_form, "comment_form": comment_form,
                   "message": message, "comments": comments, "on_watchlist": on_watchlist})


def categories_view(request):
    return render(request, "auctions/categories.html", {"category_choices": Listing.CATEGORY_CHOICES})


@login_required(login_url="/login")
def user_view(request, user_id):
    try:
        seller = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404("User not found.")
    listings = Listing.objects.filter(user=user_id)
    return render(request, "auctions/user.html", {"seller": seller, "listings": listings})


@login_required(login_url="/login")
def watchlist_view(request):
    listings = Watchlist.objects.get(user=request.user).listings.all()
    return render(request, "auctions/watchlist.html", {"listings": listings})


def category_view(request, abbreviation):
    abbreviation = abbreviation.upper()
    full_name = dict(Listing.CATEGORY_CHOICES).get(abbreviation)
    category_choice = CategoryChoice(abbreviation, full_name)
    listings = Listing.objects.filter(category=abbreviation, buyer__isnull=True)
    return render(request, "auctions/category.html", {"category_full_name": category_choice.full_name, "listings": listings})


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

        # create a watchlist for the user
        watchlist = Watchlist(user=request.user)
        watchlist.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")