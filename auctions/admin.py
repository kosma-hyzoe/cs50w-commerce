from django.contrib import admin

from .models import Listing, User, Comment, Bid


class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "starting_bid", "user", "posted_datetime")
    actions = ['delete_selected']

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    actions = ['delete_selected']


class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "value", "posted_datetime")
    actions = ['delete_selected']

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "posted_datetime")
    actions = ['delete_selected']

admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
