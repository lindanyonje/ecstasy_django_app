from wsgiref.validate import validator
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Customer(models.Model):
    name=models.CharField(max_length=100, null=False, blank=False)
    phone_number=models.IntegerField(null= True, blank= True)
    email=models.EmailField(max_length=100, null=False, blank=False)
    password=models.CharField(max_length=100, null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name=models.CharField(max_length=100, null=False, blank=False)
    cost=models.IntegerField(null= False, blank= False)
    quantity=models.IntegerField(null= False, blank= False)
    description=models.TextField(null=False, blank=False)
    image=models.FileField(upload_to='images')
    featured=models.BooleanField(default=False)
    rating=models.IntegerField(default=0, blank=True)
    status=models.CharField(max_length=100, null=False, blank=True, default='Unverified')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name=models.CharField(max_length=100, null=False, blank=False)
    parent_id=models.ForeignKey('category',on_delete=models.CASCADE,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=False)


    def getNumberOfRecipes(self):
        return self.recipe_set.all().count()


    def __str__(self):
        return self.name


class Recipe(models.Model):

    CATEGORY=(
        ('Breakfast/Brunch', 'Breakfast/Brunch'),
        ('Main Dishes', 'Main Dishes'),
        ('Salads','Salads'),
        ('Soup', 'Soup'),
        ('Meat', 'Meat'),
        ('Drinks', 'Drinks'),
        ('Appetizers', 'Appetizers'),
        ('Desserts', 'Desserts'),
        ('AirFryer', 'AirFryer'),
    )
    
  
    parent_category = models.ForeignKey(Category, null=True, blank=False, on_delete=models.SET_NULL)
    title=models.CharField(max_length=100, null=True, blank=False)
    image=models.FileField(upload_to='images')
    description=models.TextField(null=False, blank=False)
    ingridients = models.TextField(null=False, blank=False,default='SOME STRING')
    instructions = models.TextField(null=False, blank=False,default='SOME STRING')
    rating = models.IntegerField(null= True, blank= True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    
    def get_ingridients_list(self):
        return self.ingridients.split('\n')
    
    def get_instructions_list(self):
        return self.instructions.split('\n')


class Order(models.Model):
    total=models.IntegerField(null= False, blank= True)
    status=models.CharField(max_length=100, null=False, blank=False, default="Pending")
    shipping_cost=models.IntegerField(null= True, blank= True)
    order_number=models.CharField(max_length=100, null=False, blank=False)
    customer_id=models.ForeignKey('customer',on_delete=models.CASCADE,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_number


class Wishlist(models.Model):
    product_id= models.ForeignKey('product',on_delete=models.CASCADE,blank=True,null=True)  
    customer_id= models.ForeignKey('customer',on_delete=models.CASCADE,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)
  
class Cart(models.Model):
    order_id= models.ForeignKey('order',on_delete=models.CASCADE,blank=True,null=True, related_name='carts')
    product_id=models.ForeignKey('product',on_delete=models.CASCADE,blank=True,null=True)
    quantity=models.IntegerField(null= False, blank= False) 
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True) 

class Payment(models.Model):
    order_id= models.ForeignKey('order',on_delete=models.CASCADE,blank=True,null=True)
    amount=models.IntegerField(null= True, blank= True)
    description=models.TextField(null=True, blank=True)
    invoice_number=models.CharField(max_length=100, null=False, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number



class Offer(models.Model):
    product_id= models.ForeignKey('product',on_delete=models.CASCADE,blank=True,null=True)  
    offer_amount=models.IntegerField(null=False, blank=False) 
    start_date=models.DateTimeField(null=False, blank=False)
    end_date=models.DateTimeField(null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)



class Checkout(models.Model):
     customer = models.ForeignKey('customer', on_delete=models.CASCADE)
     phonenumber = models.CharField(max_length=20, null=False)
     total = models.FloatField(default=0)
     order_number = models.CharField(max_length=10, null=False)
     amount_paid = models.FloatField(default=0, )
     shipping_cost = models.FloatField(default=0)
     address = models.CharField(max_length=300, null=True, blank=True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     
     CHECKOUT_STATUS = (
         ('PENDING', 'Pending'),
         ('PAID', 'Paid'),
     )
     status = models.CharField(choices=CHECKOUT_STATUS, max_length=100, default='PENDING')  



class Inquiry(models.Model):
    name=models.CharField(max_length=100, null=False, blank=False)
    email=models.CharField(max_length=100, null=False, blank=False)
    phone_number=models.IntegerField(null= True, blank= True)
    message=models.TextField(null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Rating(models.Model):
    score= models.IntegerField(default=0, 
       validators=[
           MaxValueValidator (5),
           MinValueValidator (0),
       ]
    ) 
    def __str__(self):
      return str(self.pk)


class Review(models.Model):

    STATUS=(
        ('pending', 'pending'),
        ('approved', 'approved'),
    )
    rating= models.IntegerField(null=False, blank=False) 
    review=models.TextField( null=True, blank=True)
    customer_id=models.ForeignKey('Customer',on_delete=models.CASCADE, blank=True,null=True)
    recipe_id=models.ForeignKey('recipe',on_delete=models.CASCADE,blank=True,null=True)
    product_id=models.ForeignKey('product',on_delete=models.CASCADE,blank=True,null=True)
    status=models.CharField(max_length=100, default="pending", choices=STATUS)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def getRatingRange(self):

        return range(self.rating) 



  

















