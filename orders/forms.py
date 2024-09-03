from django import forms
from localflavor.us.forms import USZipCodeField

from .models import Order, Contact

class OrderCreateForm(forms.ModelForm):
    postal_code = USZipCodeField()
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'country', 'city']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
                
# class ShipAddCreateForm(forms.ModelForm):
#     class Meta:
#         model = ShipDetails
#         fields = ['first_name', 'last_name', 'address',
#                   'postal_code', 'country', 'city']