from django.forms import ModelForm
from auctions.models import Listing

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'