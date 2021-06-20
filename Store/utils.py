import json
from .models import *

def getCookieCart(request):
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}

	print(cart)
	items = []
	order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
	cartItems =order['get_cart_items']
	for i in cart:
		try:
			cartItems += cart[i]['quantity']
			product = Product.objects.get(id=i)

			total = (product.price * cart[i]['quantity'])
			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]['quantity']
			item ={'product':{'id':product.id,'name':product.name,'price':product.price,'imageURL':product.imageURL},'quantity':cart[i]['quantity'],'get_total':total}
			items.append(item)

			if product.digital == False:
				order['shipping'] = True
		except:
			pass
	return {'items':items , 'order':order ,'cartItems':cartItems}

def cartData(request):
	if 'userfirstname' in request.session:
		customer = Customer.objects.get(email=request.session['email'])
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cookieData = getCookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']
	return {'items':items , 'order':order ,'cartItems':cartItems}

def guestOrder(request,data):
	name = data['form']['name']
	email = data['form']['email']
	cookieData = getCookieCart(request)
	items = cookieData['items']

	customer,created = Customer.objects.get_or_create(email=email)
	customer.name=name
	customer.save()
	order, created = Order.objects.get_or_create(customer= customer,complete=False)
	print("========================================")
	print('Order3=',order)
	print("========================================")
	for item in items:
		product = Product.objects.get(id=item['product']['id']) 

		orderItem = OrderItem.objects.create(order=order,product=product,quantity=item['quantity'])
	return order ,customer