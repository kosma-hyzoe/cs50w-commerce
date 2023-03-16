from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from . import forms
from .models import User, Listing, Bid, CategoryChoice, Comment


def index(request):
    return render(request, "auctions/index.html",
                  {"listings": Listing.objects.filter(active=True).order_by('-posted_datetime')})


def archive(request):
    return render(request, "auctions/archive.html",
                  {"listings": Listing.objects.filter(active=False).order_by('-posted_datetime')})


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


def listing_view(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        highest_bid = Bid.objects.filter(listing=listing).order_by("-value").first()
    except Bid.DoesNotExist:
        highest_bid = None
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")

    message = None
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

    your_bid_form = forms.YourBid()
    comment_form = forms.CommentForm()

    comments = Comment.objects.filter(listing=listing).order_by("-posted_datetime")
    return render(request, "auctions/listing.html",
                  {"listing": listing, "highest_bid": highest_bid,
                   "your_bid_form": your_bid_form, "comment_form": comment_form,
                   "message": message, "comments": comments})


def categories_view(request):
    return render(request, "auctions/categories.html", {"category_choices": Listing.CATEGORY_CHOICES})


def user_view(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404("User not found.")
    listings = Listing.objects.filter(user=user_id)
    return render(request, "auctions/user.html", {"user": user, "listings": listings})


def category_view(request, abbreviation):
    abbreviation = abbreviation.upper()
    full_name = dict(Listing.CATEGORY_CHOICES).get(abbreviation)
    category_choice = CategoryChoice(abbreviation, full_name)
    listings = Listing.objects.filter(category=abbreviation)
    return render(request, "auctions/category.html", {"category_full_name": category_choice.full_name, "listings": listings})


def item_sold(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    item_title = listing.title
    highest_bid = Bid.objects.filter(listing=listing).order_by("-value").first()
    return None


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
