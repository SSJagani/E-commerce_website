from django.urls import path
from . import views

urlpatterns = [
	path('login',views.login,name='Login'),
	path('logout',views.logout,name='Logout'),
	path('signup',views.signup,name='Signup'),
	path('emailcheck',views.emailcheck,name='EmailCheck'),
    
    path('',views.store,name='Store'),
    path('order',views.viewAllOrder,name='Order'),
    path('cart',views.cart,name='Cart'),
    path('checkout',views.checkout,name='Checkout'),
    path('cancel_order',views.cancelOrder,name='Cancelorder'),
    path('product_view/<int:code>/Ref',views.product_view,name='Product_view'),

    path('update_item',views.updateItems,name='updateItems'),
    path('process_order',views.processOrder,name='processOrder'),

    path("sendemail",views.sendmailorder,name='sendmail')
]