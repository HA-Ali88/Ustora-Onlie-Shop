from django import forms
from .models import Review, Subscriber

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['email', 'rating', 'comment']
        
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']