from django.urls import path,include
from . import views
from django.conf import settings

from django.conf.urls.static import static
from ecstasy.views import *


urlpatterns=[
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name="home"),
    path('dashboard/',views.adminDashboard,name="dashboard"),


    path('recipe/', views.recipe, name="recipe"),
    path('update_recipe/<pk>/', views.updateRecipe, name="update_recipe"),
    path('delete_recipe/<pk>/', views.deleteRecipe, name="delete_recipe"),
    path('category/recipes', views.getCategoryRecipe, name="category_recipes"),

    path('recipes/details/<id>', views.singleRecipe, name="recipe_details"),
    path('all_recipes/', views.getRecipe, name="all_recipes"),

    path('category/details/<id>', views.getCategoryRecipes, name="get_category_recipes"),


    path('customer/', views.customer, name="customer"),
    path('customer/detail/<pk>',CustomerDetail.as_view(),name= "Customer_detail"),
    path('update_customer/<pk>/', views.updateCustomer, name="update_customer"),
    path('delete_customer/<pk>/', views.deleteCustomer, name="delete_customer"),


    path('orders/', views.getOrders, name="order_list"),
    path('order/detail/<pk>', OrderDetail.as_view(),name="Order_detail"),
    # path('order/checkout/<id>', views.checkoutOrder,name="checkout.order"),
    # path('create_order/', views.orderDetail, name="order"),
    path('update_order/<pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<pk>/', views.deleteOrder, name="delete_order"),
    path('order/mark/completed', views.markAsComplete, name="mark_as_complete"),


    path('messages/',views.inquiry, name= 'inquiry'),
    path('create/inquiry/',views.createInquiry, name= 'create.inquiry'),



    path('payment/',views.getPayment, name= 'payment'),
    path('update_payment/<pk>/', views.updatePayment, name="update_payment"),
    path('delete_payment/<pk>/', views.deletePayment, name="delete_payment"),


    path('review/',views.review, name= 'review'),
    path('delete_review/<pk>/', views.deletereview, name="delete_review"),
    path('create/review/',views.createReview, name= "create.review"),
    path('update/review/<pk>/',views.updateReviewStatus, name= "update_review"),


    path('offer/',views.getOffers, name= 'offers'),
    path('update_offer/<pk>/', views.updateOffer, name="update_offer"),
    path('delete_offer/<pk>/', views.deleteOffer, name="delete_offer"),
    path('offer_list/',views.getOfferList, name= 'offer_list'),


    # front end urls

    path('add/to/cart', views.addToCart, name="add_cart"),
    path('add/to/wishlist', views.addToWishlist, name="add_wishlist"),
    path('ajax/delete/cart',views.deleteCart,name="ajax_delete_cart"),
    path('ajax/delete/wishlist',views.deleteWishlist,name="ajax_delete_wishlist"),
    path('cart/', views.get_cart, name="cart"),
    path('wishlist/', views.get_wishlist, name="wishlist"),
    path('add/wishlist/cart',views.wishlistToCart,name="wishlist_cart"),
    path('add/cart/wishlist',views.cartToWishlist,name="cart_wishlist"),

    path('search/', views.SearchResult.as_view(), name="search_product"),


    path('complete/order', views.ordercomplete, name="order_complete"),
    path('order/mark/completed', views.markAsComplete, name="mark_as_complete"),
    path('checkout/details/<total>', views.checkoutDetails, name="checkout_details"),
    path('complete/checkout/', views.finalizeCheckout, name="complete_checkout"),


    path('shop/', views.shop, name="shop"),
    path('about/', views.getAboutMe, name="about"),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
