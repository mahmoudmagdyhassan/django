from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from django.shortcuts import render, redirect

from .models import *
from django.http import HttpResponse
from django.contrib.auth import aauthenticate,login

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .froms import Login_Form,UserCreationForms
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Product


def user_login(request):
    if request.method == 'POST':
        form = Login_Form()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = Login_Form()
    return render(request, 'store/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForms(request.POST)  # استخدام النموذج الصحيح هنا
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # استخدام 'password1' لـ UserCreationForm
            user = authenticate(request, username=username, password=password)
            login(request, user)
            # إنشاء كائن Customer للمستخدم الجديد
            Customer.objects.create(user=user, name=username, email=user.email)
            return redirect('store')
        else:
            messages.error(request, "اسم المستخدم أو كلمة المرور غير صالحة")

    else:
        form = UserCreationForms()  # نموذج جديد للطلبات GET

    return render(request, 'store/signup.html', {'form': form})

def logout_(request):
    logout(request)
    return redirect('login')


def view_description_product(request, product_id):
    print(f"Fetching product with ID: {product_id}")  # Debug statement
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    print(f"Product found: {product}")  # Debug statement
    return render(request, 'store/view.html', context)



def store(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer , complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0,'get_car_items':0}
		cartItems = order['get_cart_items']

	products = Product.objects.all()
	context = {
		"order":order,
		'items':items,
		'cartItems':cartItems,
		'products':products,

	}
	return render(request, 'store/store.html', context)

def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		# استخدم الكائن order للوصول إلى العناصر المرتبطة به
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items


	else:
		items = []
		order = {'get_car_total':0,
				 'get_car_items':0}
		cartItems = order['get_cart_items']


	context = {'items': items,
			   'order':order,
			   'cartItems':cartItems
			   }
	return render(request, 'store/cart.html', context)
def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		# استخدم الكائن order للوصول إلى العناصر المرتبطة به
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items

	else:
		items = []
		order = {'get_car_total':0,
				 'get_car_items':0}
		cartItems = order['get_cart_items']


	context = {'items': items,
			   'order':order,
			   'cartItems':cartItems
			   }
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)