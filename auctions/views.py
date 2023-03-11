from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing


def index(request):
    print(authenticate())
    return render(request, "auctions/index.html", {"listings": Listing.objects.all()})


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


def listing_view(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    return render(request, "auctions/listing.html", {"listing": listing})


def user_view(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404("User not found.")
    listings = Listing.objects.filter(user=user_id)
    return render(request, "auctions/user.html", {"user": user, "listings": listings})


def create(request):
    if request.method == "POST":
        listing = Listing(
            user_id=request.user,
            listing_title=request.POST.get("title"),
            description=request.POST.get("description"),
            starting_bid=request.POST.get("starting-bid"),
            image_url=request.POST.get("image-link"),
            category=request.POST.get("category")
        )
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    elif request.method == "GET":
        return render(request, "auctions/create.html")