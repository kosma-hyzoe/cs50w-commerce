from django.contrib import admin

from .models import Listing, User


class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "starting_bid", "user")


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")


admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)