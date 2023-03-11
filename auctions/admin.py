from django.contrib import admin

from .models import Listing


class ListingAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user")


admin.site.register(Listing, ListingAdmin)