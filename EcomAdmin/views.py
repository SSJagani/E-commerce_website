from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from Store.models import Customer,Product,Order,OrderItem,ShippingAddress,Categories
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json
# Create your views here.


def index(request):
	if request.method == 'POST':
		email = request.POST['a_email'].lower()
		password = request.POST['a_password']
		if Customer.objects.filter(email=email,user_code=1).exists():
			login_result = Customer.objects.filter(email=email,password=password,user_code=1)
			if login_result.exists():
				data = dict(login_result.values()[0])
				request.session['Adminfirstname'] = data['first_name']
				request.session['adminemail'] = data['email']
				messages.success(request , "Successfully Login Your Account....")
				return redirect('Admin-Store')
			else:
				messages.error(request , "Password Dose Not Match...")
				return render(request,"admin/login.html")
		else:
			messages.error(request , "Your Are Not Admin...")
			return render(request,"admin/login.html")
	else:
		if 'Adminfirstname' in request.session:
			return redirect('Admin-Store')
		else:
			return render(request,"admin/login.html")

def adminlogout(request):
	if 'Adminfirstname' in request.session and 'adminemail' in request.session:
		del request.session['Adminfirstname']
		del request.session['adminemail']
		messages.success(request , "Successfully Logout Your Account....")
		request.session.clear_expired()
		return redirect('Admin-Home')
	else:
		return redirect('Admin-Home')

def adminstore(request):
	if 'Adminfirstname' in request.session and 'adminemail' in request.session:
		prodeuct_name = Product.objects.all()
		context = {'Products': prodeuct_name}
		return render(request,'admin/admin-store.html',context)
	else:
		return redirect('Admin-Home')


def product_view(request, code):
	if 'Adminfirstname' in request.session and 'adminemail' in request.session:
		product = Product.objects.get(id = code)
		context = {'product':product}
		return render(request , "admin/view.html",context)
	else:
		return redirect('Admin-Home')

def product_edit(request,code):
	if 'Adminfirstname' in request.session and 'adminemail' in request.session:
		if request.method == 'POST':
			product = Product.objects.get (id=code)
			print(product)
			product_name = request.POST['product_name']
			product_price = request.POST['price']
			product_category =request.POST['category']
			product_description = request.POST['description']
			product_digital = request.POST['digital']
			catgory = Categories.objects.get(id=product_category)
			if 'image' in request.FILES:
				product_image = request.FILES['image']
				product.image = product_image
			product.name = product_name
			product.price = product_price
			product.category = catgory
			product.Description = product_description
			product.digital = product_digital
			try:
				product.save()
				return redirect("Admin-Store")
			except Exception as e:
				messages.error(request , e)
				return redirect("Admin-Store")
		else:
			try:
				product = Product.objects.filter(id=code)
				catgory = Categories.objects.all()
				context = {'product':product,'catgorys':catgory}
				return render(request,'admin/add-product.html',context)
			except Exception as e:
				print(e)
				messages.error(request , "Product Id Dose Not Exists...")
				return redirect('Admin-Store')
	else:
		return redirect('Admin-Home')



def product_delete(request):
	if 'Adminfirstname' in request.session and 'adminemail' in request.session:
		if request.method == 'POST':
			productId = json.loads(request.body)['productId']
			product = Product.objects.get(id = productId)
			try:
				product.delete()
				# messages.success(request , "Successfully delete Your Item....")
				return JsonResponse('Successfully delete Your Item',safe=False)
			except Exception as e:
				messages.error(request , e)
				return redirect("Admin-Store")
		else:
			return redirect('Admin-Store')
	else:
		return redirect('Admin-Home')



def addproduct(request):
	if 'Adminfirstname' in request.session and 'adminemail' in request.session:
		if request.method == 'POST':
			product_name = request.POST['product_name']
			product_price = request.POST['price']
			product_category =request.POST['category']
			product_description = request.POST['description']
			product_digital = request.POST['digital']
			product_image = request.FILES['image']
			print(product_name,product_price,product_category,product_description,product_digital,product_image)
			catgory = Categories.objects.get(id=product_category)
			product = Product(name=product_name,price=product_price,category=catgory,Description=product_description,digital=product_digital,image=product_image)
			product.save()
			messages.success(request , "Successfully Add Your Item....")
			return redirect('Admin-Store')
		else:
			catgory = Categories.objects.all()
			context = {'catgorys':catgory}
			return render(request, 'admin/add-product.html',context)
	else:
		return redirect('Admin-Home')

def completeOrder(request):
	if "Adminfirstname" in request.session and 'adminemail' in request.session:
		order = Order.objects.all().filter(sipping_complete=True,complete=True)
		page = request.GET.get('page', 1)
		paginator = Paginator(order, 10)
		try:
			order = paginator.page(page)
		except PageNotAnInteger:
			order = paginator.page(1)
		except EmptyPage:
			order = paginator.page(paginator.num_pages)

		return render(request,"admin/complete-order.html",{'orders':order})
	else:
		return redirect('Admin-Home')

def notcompleteOrder(request):
	if "Adminfirstname" in request.session and 'adminemail' in request.session:
		order = Order.objects.all().filter(sipping_complete=False,complete=True).order_by('id')
		page = request.GET.get('page', 1)
		paginator = Paginator(order, 10)
		try:
			order = paginator.page(page)
		except PageNotAnInteger:
			order = paginator.page(1)
		except EmptyPage:
			order = paginator.page(paginator.num_pages)

		return render(request,'admin/not-complete-order.html',{'orders':order})
	else:
		return redirect('Admin-Home')

def orderview(request,code):
	if 'Adminfirstname' in request.session and 'adminemail' in request.session:
		order = Order.objects.get(id=code)
		shipping_address = ShippingAddress.objects.get(order=order)
		items = order.orderitem_set.all()
		return render(request,'admin/order-view.html',{'order':order,'items':items,'address':shipping_address})
	else:
		return redirect('Admin-Home')

def shippingcomplete(request):
	if 'Adminfirstname' in request.session and 'adminemail' in request.session:
		if request.method == 'POST':
			orderId = json.loads(request.body)['orderId']
			order = Order.objects.get(id=orderId)
			order.sipping_complete = True
			try:
				order.save()
				messages.success(request , "Successfully Update Shipping Complete This  Order"+orderId+".")
				return JsonResponse("Successfully Update Shipping Complete This  Order"+orderId+".", safe=False)
			except Exception as e:
				messages.error(request , e)
				return redirect('Admin-Not-Complete-Order')
			return JsonResponse("Successfully Done...",safe=False)
		else:
			return HttpResponse(code)
	else:
		return redirect('Admin-Home')