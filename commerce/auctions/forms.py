from django import forms

class CreateListingForm(forms.Form):
    title = forms.CharField(max_length=64, label="Title:")
    starting_price = forms.DecimalField(max_digits=10, decimal_places=2, label="Starting Price:")
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={
        "rows": 20,
        "columns": 100
    }))
    category = forms.CharField(required=False, max_length=64, label="Category:")
    url_image = forms.URLField(label="Image(URL):", required=False)

class PlaceBidForm(forms.Form):
    bid_value = forms.DecimalField(max_digits=10, decimal_places=2, label="Bid:")