from django.forms import ModelForm, FloatField, ImageField
from auctions.models import Listing, Comment, Category
from django.forms.widgets import Widget

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'

    starting_bid = FloatField(required=False)
    #image = ImageField(widget=ImageWidget)

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
        labels = {'text': 'Your comment'}