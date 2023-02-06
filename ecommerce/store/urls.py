from . import views
from django.urls import path



urlpatterns =[
    path('login/', views.loginPage, name='login'),
    path('logout/', views.LogoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('', views.store, name='store'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:pk>', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:item_id>/', views.update_cart, name='update_cart')

    
]