from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
import json
import datetime
from .utils import *
from django.contrib import messages
from .models import Customer,Product,Order,OrderItem,ShippingAddress

import smtplib, ssl

# Create your views here.

def login(request):
	if request.method == 'POST':
		email = request.POST['l_email'].lower()
		password = request.POST['pass']
		if Customer.objects.filter(email=email).exists():
			login_result = Customer.objects.filter(email=email,password=password)
			if login_result.exists():
				data = dict(login_result.values()[0])
				request.session['userfirstname'] = data['first_name']
				request.session['email'] = data['email']
				messages.success(request , "Successfully Login Your Account....")
				return redirect('Store')
			else:
				messages.error(request , "Password Dose Not Metch...")
				return redirect('Store')
		else:
			messages.error(request , "Email Address Dose Not Exists...")
			return redirect('Store')
	else:
		return redirect('Store')

def logout(request):
	if 'userfirstname' in request.session and 'email' in request.session:
		del request.session['userfirstname']
		del request.session['email']
		messages.success(request , "Successfully Logout Your Account....")
		request.session.clear_expired()
		return redirect('Store')
	else:
		return redirect('Store')

def signup(request):
	if request.method == 'POST':
		first_name = request.POST['f_name']
		last_name = request.POST['l_name']
		user_name = request.POST['user_name']
		email = request.POST['s_email'].lower()
		password = request.POST['password']
		c_password = request.POST['c_password']
		if len(password) >= 6:
			if password == c_password:
				print(first_name,last_name,user_name,email,password,c_password)
				customer = Customer(first_name=first_name,last_name=last_name,user_name=user_name,email=email,password=password)
				customer.save()
				messages.success(request , "Successfully Registration Your Account....")
				return redirect('Store')
			else:
				messages.error(request , "Password and Conform Password Not Metch...")
				return redirect('Store')
		else:
			messages.error(request , "Password Lengtn Below 6 digit....")
			return redirect('Store')
	else:
		messages.error(request , "This Method Not Allow....")
		return redirect('Store')

def emailcheck(request):
	if request.method == 'POST':
		email = json.loads(request.body)['email'].lower()
		result = Customer.objects.filter(email=email).exists()
		if not result:
			return JsonResponse(2002,safe=False)
		else:
			return JsonResponse(2001,safe=False)
	else:
		messages.error(request , "This Method Not Allow....")
		return JsonResponse("This Method Not Allow...",safe=False)

def store(request):
	prodeuct_name = Product.objects.all()
	data = cartData(request)
	cartItems = data['cartItems']
	context = {'Products': prodeuct_name,'cartItems':cartItems}
	return render(request,'store/store.html',context)

def cart(request):
	cookieData = cartData(request)
	cartItems = cookieData['cartItems']
	order = cookieData['order']
	items = cookieData['items']
	if items:
		context = {'items':items , 'order':order ,'cartItems':cartItems}
		return render(request,'store/cart.html',context)
	else:
		messages.error(request , "Cart Is Empty....")
		return redirect('Store')
def checkout(request):
	cookieData = cartData(request)
	cartItems = cookieData['cartItems']
	order = cookieData['order']
	items = cookieData['items']
	if items:
		context = {'items':items , 'order':order ,'cartItems':cartItems}
		return render(request,'store/checkout.html',context)
	else:
		messages.error(request , "Cart Is Empty....")
		return redirect('Store')

def updateItems(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		productId = data['productId']
		action = data['action']
		print('productId ', productId)
		print('action ',action)
		email_data = request.session['email']
		print(email_data)
		customer = Customer.objects.get(email=email_data)
		product = Product.objects.get(id=productId)
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)
		if action == 'add':
			orderItem.quantity = (orderItem.quantity + 1)
		elif action == 'remove':
			orderItem.quantity = (orderItem.quantity - 1)
		orderItem.save()

		if orderItem.quantity <= 0:
			orderItem.delete()

		return JsonResponse('Item was added...',safe=False)
	else:
		return HttpResponse('This Method Not Allow..')

def processOrder(request):
	print('Data :',request.body)
	transection_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	if 'userfirstname' in request.session:
		customer = Customer.objects.get(email=request.session['email'])
		order = Order.objects.get(customer= customer,complete=False)
		print('Order2=',order)
		# print('created=',created)

	else:
		print('User not update..')

		print("Cookie: ",request.COOKIES)
		order,customer = guestOrder(request,data)

	total = float(data['form']['total'])
	print(transection_id)
	order.transaction_id = transection_id
	if total == order.get_cart_total:
		print('if')
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)
	messages.success(request,"Successfully Place Your Order.....")
	return JsonResponse('Payment Complete...',safe=False)

def product_view(request, code):
	product = Product.objects.get(id = code)
	data = cartData(request)
	cartItems = data['cartItems']
	context = {'product':product,'cartItems':cartItems}
	return render(request , "store/view.html",context)

def viewAllOrder(request):
	if 'email' in request.session:
		user_email = request.session['email']
		customer = Customer.objects.get(email=user_email)
		order = Order.objects.filter(customer=customer,complete = True)
		print(order)
		order_data={}
		for i in order:
			print('order=',i.get_cart_items)
			item = i.orderitem_set.all()
			order_data[i] = list(item)
		print(order_data)
		data = cartData(request)
		cartItems = data['cartItems']
		context = {'orders':order_data,'cartItems':cartItems}
		return render(request, 'store/order.html', context)
	else:
		messages.error(request , "Please Login With Your Registre Email Address.. ")
		return redirect('Store')

def cancelOrder(request):
	if request.method == 'POST':	
		orderId = json.loads(request.body)['orderId']
		order = Order.objects.get(id=orderId)
		order.cancel_order = True
		order.save()
		messages.warning(request , "Successfully Cancel Your Order....")
		return JsonResponse('Order Is Successfully Delete...',safe=False)
	else:
		return HttpResponse('This Method Not Allow..')

def sendmailorder(request):
	smtp_server = "smtp.gmail.com"
	port = 452  # For starttls
	sender_email = "peterapps70@gmail.com"
	password = "United999"
	message = "your order is Accepted..."
	receiver_email = 'peterapps50@gmail.com'

	# Create a secure SSL context
	context = ssl.create_default_context()

	# Try to log in to server and send email
	try:
		server = smtplib.SMTP(smtp_server,port)
		server.ehlo() # Can be omitted
		server.starttls() # Secure the connection
		server.ehlo() # Can be omitted
		server.login(sender_email, password)
		# TODO: Send email here
		server.sendmail(sender_email, receiver_email, message)
		server.quit() 
	except Exception as e:
		# Print any error messages to stdout
		print(e)
	return HttpResponse("Done.............")