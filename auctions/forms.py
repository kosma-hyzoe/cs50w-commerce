from django import forms

from .models import Listing


class CreateNewListing(forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea, max_length=2000)
    starting_bid = forms.DecimalField(label="Starting Bid (USD)", decimal_places=2, max_digits=10)
    image_link = forms.URLField(label="Image Link", required=False)
    category = forms.ChoiceField(label="Category", choices=Listing.CATEGORY_CHOICES, required=False)


class YourBid(forms.Form):
    value = forms.DecimalField(label="Your Bid: ", label_suffix="$", decimal_places=2, max_digits=10)


class CommentForm(forms.Form):
    content = forms.CharField(label="Your Comment: ", max_length=200, widget=forms.Textarea(attrs={"rows": 4}))