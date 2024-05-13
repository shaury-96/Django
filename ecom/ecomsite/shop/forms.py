# from stripe import Review
from .models import ProductReview
from django import forms

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Write a review'}))
    class Meta:
        model = ProductReview
        fields = ['rating','review']
        # fields[0].label=""
       

    def __init__(self, *args, **kwargs):
        super(ProductReviewForm, self).__init__(*args, **kwargs)
        self.fields['rating'].label = "" 
        self.fields['review'].label = "" 