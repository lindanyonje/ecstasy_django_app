from django.forms import ModelForm

from .models import *


class OrderForm(ModelForm):
    class Meta:
        model= Order
        fields= ['customer_id',  'status', 'total']

class RecipeForm(ModelForm):
    class Meta:
        model= Recipe
        fields= '__all__'              

class CustomerForm(ModelForm):
    class Meta:
        model= Customer
        fields= '__all__'

class ProductForm(ModelForm):
    class Meta:
        model= Product
        fields= '__all__'        

class PaymentForm(ModelForm):
    class Meta:
        model= Payment
        fields= '__all__' 


class OfferForm(ModelForm):
    class Meta:
        model= Offer
        fields= '__all__'

        
class InquiryForm(ModelForm):

    class Meta:
        model = Inquiry
        fields= '__all__'    

       
class ReviewForm(ModelForm):

    class Meta:
        model = Inquiry
        fields= '__all__'                                                   