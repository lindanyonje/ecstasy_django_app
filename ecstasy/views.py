from django.shortcuts import render
from email import message
from logging.handlers import RotatingFileHandler
from multiprocessing import context
from django.db import IntegrityError
from django.http.response import JsonResponse
from unicodedata import category
from django.shortcuts import render,redirect
from django .http import HttpResponse, HttpResponseRedirect
from django .forms import inlineformset_factory
from .models import*
from .forms import OfferForm, OrderForm, CustomerForm,RecipeForm,PaymentForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .filters import OrderFilter
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.dispatch import receiver

# Create your views here.



def home(request):

   reviews = Review.objects.filter(status = "approved")[:6] 
   recipes = Recipe.objects.all()[:3]
   products = Product.objects.all()[:3]
   categories= Category.objects.all()
   wishlist = Wishlist.objects.all()
   cart = Cart.objects.all()
 
   # category = Category.objects.get(name="Recipes")

   context = {
      'reviews' :reviews,
      'recipes' :recipes,
      'products': products,
      'categories': categories,
      'wishlist': wishlist,
      'cart' : cart,
   }

   return render(request, 'ecstasy/frontend/home.html', context)

def adminDashboard(request):


   orders= Order.objects.all()
   
   customers= Customer.objects.all()

   total_customers = customers.count()

   payment = Payment.objects.all()

   recipe= Recipe.objects.all()

   offers= Offer.objects.all()

   total_orders = orders.count()

   completed = orders.filter(status='completed').count()

   pending = orders.filter(status='pending').count()

   context = {
      'orders': orders, 
      'customers': customers, 
      'total_custmers' : total_customers,
      'total_orders': total_orders, 
      'completed': completed, 
      'pending':pending, 
      'payment':payment, 
      'recipe':recipe, 
      'offers':offers, }

    ##Declaring a dictionary used to package the data we shall
    ##send to the frontend html template for display.

 
   context={}



   return render(request, 'ecstasy/admin/dashboard.html', context)   


def customer(request):

   customers = Customer.objects.all()

   orders= Order.objects.all()
   total_orders = orders.count()
   myFilter= OrderFilter(request.GET, queryset=orders)

   # orders = Customer.order_set.all()

   orders= myFilter.qs

   context = {'customers':customers,'orders': orders,'total_orders': total_orders, 'myFilter': myFilter}

   return render(request, 'ecstasy/admin/Customer/customer.html', context)   

@login_required
def updateCustomer(request, pk):

   customer = Customer.objects.get(id=pk)
   form=CustomerForm(instance=customer)

   if request.method == 'POST':
  
      form=CustomerForm(request.POST, instance=customer)
      if form.is_valid():
         form.save()
         return redirect('/customer')

   context= {'form':form}

   return render(request, 'ecstasy/admin/Customer/customer_form.html', context)   

 

@login_required
def deleteCustomer(request, pk):

   customer = Customer.objects.get(id=pk)

   if request.method == 'POST':
      customer.delete()
      return redirect('/customer')

   context= {'item': customer}

   return render(request, 'ecstasy/admin/Customer/customer_delete.html', context)  


class CustomerList(LoginRequiredMixin, ListView):

    login_required= True
    model = Customer
    template_name= 'ecstasy/admin/Customer/customer_list.html'


class CustomerDetail(LoginRequiredMixin, DetailView):

    login_required= True
    model =  Customer
    template_name= 'ecstasy/admin/Customer/customer_details.html'



@login_required
class OrderList(ListView):

    login_required= True
    model =Order
    template_name= "ecstasy/admin/Order/order_list.html"

class OrderDetail(LoginRequiredMixin, DetailView):

    login_required= True
    model = Order
    fields = '__all__'
    template_name= "ecstasy/admin/Order/order_details.html"


class CreateOrder(LoginRequiredMixin, CreateView):
   model = Order
   fields = '__all__'
   template_name = 'ecstasy/admin//Orderorder_form.html'
   success_url = '/dashboard'

@login_required
def getOrders(request):

   orders = Order.objects.all()

   return render(request, 'ecstasy/admin/Order/order.html', {'orders': orders})

@login_required
def createOrder(request, pk):

   customer = Customer.objects.get(id=pk)

   OrderFormSet = inlineformset_factory(Customer, Order, fields=('customer_id','service_category','status', 'total'), extra=5)

   formset= OrderFormSet(queryset=Order.objects.none(),instance=customer)
   # form= OrderForm(initial={'customer': customer})
   if request.method == 'POST':
      # print('POST:',request.POST)
      # form=OrderForm(request.POST)   
      formset= OrderFormSet(request.POST, instance=customer)
      if formset.is_valid():
         formset.save()
         return redirect('/dashboard')

   context= {'formset':formset}

   return render(request, 'ecstasy/admin/Order/order_form.html', context)      

@login_required
def updateOrder(request, pk):

   order= Order.objects.get(id=pk)
   form= OrderForm(instance=order)

   if request.method == 'POST':
  
      form=OrderForm(request.POST, instance=order)
      if form.is_valid():
         form.save()
         return redirect('/dashboard')

   context= {'form':form}

   return render(request, 'ecstasy/admin/Order/order_form.html', context)         


@login_required
def deleteOrder(request, pk):

   order= Order.objects.get(id=pk)

   if request.method == 'POST':
      order.delete()
      return redirect('/dashboard')

   context= {'item': order}

   return render(request, 'ecstasy/admin/Order/order_delete.html', context)         



class CreateRecipe(LoginRequiredMixin, CreateView):
   model = Recipe
   fields = '__all__'
   template_name = 'ecstasy/admin/Recipe/recipe_form.html'
   success_url = '/dashboard'

@login_required
def recipe(request):

   recipe = Recipe.objects.all()

   context={'recipe': recipe}

   return render(request, 'ecstasy/admin/Recipe/recipe.html', context)


@login_required
def updateRecipe(request, pk):

   recipe = Recipe.objects.get(id=pk)
   form=RecipeForm(instance=recipe)

   if request.method == 'POST':
  
      form=RecipeForm(request.POST, instance=recipe)
      if form.is_valid():
         form.save()
         return redirect('/recipe')

   context= {'form':form}

   return render(request, 'ecstasy/admin/Recipe/recipe_form.html', context)   




@login_required
def deleteRecipe(request, pk):

   recipe= Recipe.objects.get(id=pk)
   

   if request.method == 'POST':
      recipe.delete()
      return redirect('/recipe')

   context= {'item': recipe}

   return render(request, 'ecstasy/admin/Recipe/recipe_delete.html', context)         



class CreateInquiry(LoginRequiredMixin, CreateView):
   model = Inquiry
   fields = '__all__'
   template_name = 'ecstasy/admin/Inquiry/inquiry.html'
   success_url = '/dashboard'


@login_required
def inquiry(request):
   
   inquiry = Inquiry.objects.all()
  

   context = {
      'inquiries' : inquiry
   }


   return render(request, 'ecstasy/admin/Inquiry/inquiry.html', context)        



def createInquiry(request):

   f_name = request.POST.get("firstname")
   number = request.POST.get("phone_number")
   email = request.POST.get("email")
   subject = request.POST.get("subject")

   Inquiry.objects.create(
      name = f_name,
      email = email,
      phone_number = number,
      message = subject
   )

   context = {
      
   }

   return render(request, 'ecstasy/frontend/inquiry_success.html', context)      

@login_required
def review(request):

   reviews= Review.objects.all()

   context = {
      'reviews' : reviews
   }


   return render(request, 'ecstasy/admin/Review/review.html', context)  



def createReview(request):
   success=False
   message = ""
   
   if request.method == "POST":
      rating=request.POST.get("rating")
      f_name = request.POST.get("fullname")
      number = request.POST.get("phone_number")
      email = request.POST.get("email")
      subject = request.POST.get("subject")

      customer = Customer.objects.filter(email = email).first()

      if customer:
         
         try:
            
            Review.objects.create(
                  customer_id = customer,
                  rating = rating,
                  review= subject,

               )
            success=True
            message= "Thank you for your review"

            print(":::::CREATED MESSAGE::::::"+message)
         
         except IntegrityError as e:
            print("INTEGRITY ERROR: "+str(e))
            message = "INTEGRITY ERROR"+str(e)

   data = {
      "success":success,
      "message": message
   }

   return JsonResponse(data)    


@login_required      
def updateReviewStatus(request, pk):

   ##Using get can give a 404 error: Use try except
   review= Review.objects.get(id=pk)

   if "pending" in review.status:
      review.status = "approved"
   else:
      review.status = "pending"

   review.save()

   messages.success(request, 'Review updated successfully.')

   return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def deletereview(request, pk):

   review= Review.objects.get(id=pk)

   if request.method == 'POST':
      review.delete()
      return redirect('/review')

   context= {'item': review}

   return render(request, 'ecstasy/admin/Review/review_delete.html', context)     




@login_required
def getPayment(request):
   payment= Payment.objects.all()

   return render(request, 'ecstasy/admin/Payment/payment.html', {'payment':payment})   

@login_required
def updatePayment(request, pk):

   payment= Payment.objects.get(id=pk)
   form= PaymentForm(instance=payment)

   if request.method == 'POST':
  
      form=OrderForm(request.POST, instance=payment)
      if form.is_valid():
         form.save()
         return redirect('/payment')

   context= {'form':form}

   return render(request, 'ecstasy/admin/Payment/payment_form.html', context)         


@login_required
def deletePayment(request, pk):

   payment= Payment.objects.get(id=pk)

   if request.method == 'POST':
      payment.delete()
      return redirect('/payment')

   context= {'item': payment}

   return render(request, 'ecstasy/admin/Payment/payment_delete.html', context)     
     


@login_required
def getOfferList(request):
   offers= Offer.objects.all()

   return render(request, 'ecstasy/admin/Offer/offer_list.html', {'offers': offers})    



@login_required
def updateOffer(request, pk):

   offer= Offer.objects.get(id=pk)
   form= OfferForm(instance=offer)

   if request.method == 'POST':
  
      form=OfferForm(request.POST, instance=offer)
      if form.is_valid():
         form.save()
         return redirect('/offers')

   context= {'form':form}

   return render(request, 'ecstasy/admin/Offer/offer_form.html', context)         


@login_required
def deleteOffer(request, pk):

   offer= Offer.objects.get(id=pk)

   if request.method == 'POST':
      offer.delete()
      return redirect('/offers')

   context= {'item': offer}

   return render(request, 'ecstasy/admin/Offer/offer_delete.html', context)     


def getOffers(request, id):
   

   return render(request, 'ecstasyy/frontend/offer.html')   



def getRecipe(request):

   recipe = Recipe.objects.all()

   context={'recipe': recipe}

   return render(request, 'ecstasy/frontend/recipe.html', context)





def getCategoryRecipe(request):

   
   recipe = Recipe.objects.all()

   context={'recipe': recipe}


   return render(request, 'ecstasy/frontend/category.html', context)   


def getCategoryProducts(request, id):

    c_id = id
    context = {}
    context['recipes'] = Recipe.objects.filter(category_id = c_id)
    context['products'] = Product.objects.filter(category_id = c_id)

    return render(request, 'ecstasy/frontend/category.html', context)

def getProduct(request, id):

    product = Product.objects.get(pk = id)
    commentForm = ReviewForm()
    

    context = {
        'product' : product,
        'related_products' : Product.objects.filter(category_id = product.id),
        # 'reviews' : Review.objects.filter(product_id = product.id),
        'form' : commentForm,
        'rating': range(product.rating)
    }

    return render(request, 'ecstasy/frontend/detail_product.html', context)


def getCategoryProducts(request, id):

    c_id = id
    context = {}
    context['products'] = Product.objects.filter(category_id = c_id)

    return render(request, 'ecstasy/frontend/category_products.html', context)

class CategoryList(ListView):
    
    login_required= True
    model = Category
    template_name= "ecstasy/admin/category_list.html"

class CategoryDetail(DetailView):

    model = Category

class CategoryCreate(CreateView):  

    login_required= True
    model = Category
    template_name= "ecstasy/admin/category_form.html"

    #specify the fields to be displayed

    fields = '__all__'

    #function to redirect user

    def get_success_url(self):
        return reverse('Category_List') #uses the path name

class CategoryUpdate(UpdateView):

    login_required= True
    model = Category
    fields = '__all__'
    template_name= "ecstasy/admin/category_form.html"
    success_url = '/categories' #this uses the path url

class CategoryDelete(DeleteView):

    login_required= True
    model = Category
    success_url = '/categories'

    

class ProductList(ListView):

    login_required= True
    model =Product
    template_name= "ecstasy/admin/product_list.html"

class ProductDetail(DetailView):

    login_required= True
    model = Product
    template_name= "ecstasy/admin/product_detail.html"


class ProductCreate(CreateView): 

    login_required= True 
    model = Product
    template_name= "ecstasy/admin/product_form.html"
    success_url = '/categories'

    #specify the fields to be displayed

    fields = '__all__'

    #function to ridirect user

    def get_success_url(self):
        return reverse('Product')

class ProductUpdate(UpdateView):

    login_required= True
    model = Product
    fields = '__all__'
    success_url = '/products'
    template_name= "ecstasy/admin/product_form.html"


class ProductDelete(DeleteView):

    login_required= True
    model = Product
    success_url = '/products'
    template_name= "ecstasy/admin/product_confirm_delete.html"



def get_cart(request):
    cart_items = Cart.objects.filter(order_id__isnull = True)
    
    return render(request, 'ecstasy/frontend/cart.html', {'cart': cart_items})    


def get_wishlist(request):
    wishlist = Wishlist.objects.all()

    return render(request, 'ecstasy/frontend/wishlist.html', {'wishlist': wishlist})



def checkoutDetails(request, total):

    context = {
            'total' : total,
        }
    return render(request, 'ecstasy/frontend/checkout.html', context)


def finalizeCheckout(request):
    if request.method == "GET":

        return render(request, 'ecstasy/frontend/cart.html', context={})

    else:
        name=request.POST.get('name')
        email=request.POST.get('email')
        total=request.POST.get('total')
        order_number= "BURA_123_56"
        address=request.POST.get('address')
        payment_mode = request.POST.get("paymentMode")
        
        customer = Customer.objects.filter(email= email).first()
        if customer is None:
            customer = Customer.objects.create(
                name = name,
                email = email,
                password = email,
            )
        order = Order.objects.create(
            total = total,
            order_number = order_number,
            status = "Pending",
            customer_id = customer

        )

        cart_items = Cart.objects.filter(order_id__isnull = True).update(order_id = order.id)

        context = {
            'order' : order.id,
        }

        return JsonResponse(context)



def deleteCart(request):

    cart_id = request.POST.get('cart_id')
    cart_item= Cart.objects.get(pk = cart_id)
    cart_item.delete()
    

    data ={}

    return JsonResponse(data)


def addToCart(request):

    product_id = request.POST.get("product_id", None)

    quantity = request.POST.get("quantity", None)

    product = Product.objects.get(id = product_id)

    # Cart.objects.create(product_id = product, quantity = quantity)

    cart_product = Cart.objects.filter(product_id = product.id)
   #  print(cart_product)
    if not cart_product:
   
        Cart.objects.create(product_id = product, quantity= quantity)
        data ={
            'message' : "Product added to cart"
        }
    else:
        data = {
            'message' : "Product is already in cart"
        }

    return JsonResponse(data)


    

def deleteWishlist(request):

    recipe_id = request.POST.get("recipe_id", None)
   
   #  print(recipe_id)
    
    wishlist_object = Wishlist.objects.get(id = recipe_id)
   #  print(wishlist_object)
    wishlist_object.delete()

    data ={}

    return JsonResponse(data)



def addToWishlist(request):

    recipe_id = request.POST.get("recipe_id", None)
   
    recipe = Recipe.objects.get(pk =recipe_id) 

    wishlist_product = Wishlist.objects.filter(recipe_id =recipe.id)
   #  print(wishlist_product)
    if not wishlist_product:
   
        Wishlist.objects.create(recipe_id = recipe)
        data ={
            'message' : "Product added to wishlist"
        }
    else:
        data = {
            'message' : "Product is already in wishlist"
        }

    return JsonResponse(data)



def wishlistToCart(request):

   id = request.POST.get("id", None)
    
   quantity = 1

   wishlist_item = Wishlist.objects.get(pk = id)

   recipe =  wishlist_item.recipe_id

   Cart.objects.create(recipe_id = recipe, quantity = quantity)

   wishlist_item.delete()

   data ={}

   return JsonResponse(data)


def cartToWishlist(request):

    id = request.POST.get("id", None)

    # quantity = 1

    cart_item = Cart.objects.get(pk = id)

    recipe =  cart_item.recipe_id

    Wishlist.objects.create(recipe_id = recipe)

    # Cart.objects.create(product_id = product, quantity = quantity)

    cart_item.delete()

    data ={}

    return JsonResponse(data)



class SearchResult(ListView):
    model = Product
    template_name = 'ecstasy/frontend/layouts/search_results.html'

    def get_queryset(self):
        query =self.request.GET.get('search_data')
        object_list = Product.objects.filter(Q(name__icontains=query))
        # object_list = Product.objects.filter(
        #     Q(name__icontains=query | Q(state__icontains=query))
            
        # )
        return object_list


def ordercomplete(request, id):
    
    order = Order.objects.get(id = id)
    cart = Cart.objects.filter(order_id = order)
   
def markAsComplete(request):

    order_id = request.POST.get('order_id')
    print(order_id)

    order = Order.objects.get(pk = order_id)
    order.status = "Completed"
    order.save()

    data = {
        'success' : True
        }

    return JsonResponse(data)    


def singleRecipe(request, id):

    recipe = Recipe.objects.get(pk = id)
  
    

    context = {
        'recipe' : recipe,
      #   'related_recipes' : Recipe.objects.filter(category_id = recipe.id),
        # 'reviews' : Review.objects.filter(product_id = product.id),
        
        'rating': range(recipe.rating)
    }

    return render(request, 'ecstasy/frontend/detail_recipe.html', context)


def shop(request):
    

    return render(request, 'ecstasy/frontend/shop.html')


def getAboutMe(request):

   return render(request, 'ecstasy/frontend/about_me.html')        