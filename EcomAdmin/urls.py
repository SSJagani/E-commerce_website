from django.urls import path
from . import views

urlpatterns = [
	path('',views.index,name="Admin-Home"),
	path('admin-logout',views.adminlogout,name='Admin-Logout'),
	path('admin-store',views.adminstore,name='Admin-Store'),
	
	path('add-product',views.addproduct,name='Add-Product'),
	path('admin-complete-order',views.completeOrder,name='Admin-Complete-Order'),
	path('admin-not-complete-order',views.notcompleteOrder,name='Admin-Not-Complete-Order'),

	path('product_view/<int:code>/Ref=&8gQZDf1uFb',views.product_view,name='Product_view'),
	path('product_edit/<int:code>/Ref=$E2CaBHNP2R',views.product_edit,name='Product_edit'),
	path('product_delete/Ref=*sOur8Cl8s7',views.product_delete,name='Product_detele'),

	path('admin-order-view/<int:code>/ref=$goenDif85UJ',views.orderview,name='Order-View'),

	path('shipping-complete/Ref=!DerRe8F5S6Q',views.shippingcomplete,name='Shipping-Complete'),
]