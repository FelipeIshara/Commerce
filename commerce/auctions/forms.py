from django import forms

class CreateListingForm(forms.Form):
    title = forms.CharField(max_length=64, label="Title:")
    starting_price = forms.DecimalField(max_digits=10, decimal_places=2, label="Starting Price:")
    category = forms.CharField(required=False, max_length=64, label="Category:")
    url_image = forms.URLField(label="Image(URL):", required=False)
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={
        "rows": 10,
    }))
class PlaceBidForm(forms.Form):
    bid_value = forms.DecimalField(max_digits=10, decimal_places=2, label="Bid")

class CommentForm(forms.Form):
    comment = forms.CharField(label="Comment", widget=forms.Textarea(attrs={
        "rows": 1,
    }))