from itertools import product
from urllib import request
from django.shortcuts import HttpResponseRedirect, render, redirect

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages



from main.models import *
# Create your views here
def main(request):
    card = SneakerCard.objects.all()
    brand = Brand.objects.all()
    searched_sneakers = request.POST.get('search')
    product = SneakerCard.objects.filter(title = searched_sneakers)
    return render(request, 'index.html', {'product':product, 'brand':brand, 'card':card})

def more(request, id):
    more = SneakerCard.objects.get(id = id)
    return render(request, 'more.html',{'more': more} )



res = {}
def addCart(request, pk):
    cart_session = request.session.get('cart_session', [])
    print(type(cart_session))
    cart_session.append(pk)
    request.session['cart_session'] = cart_session
    return HttpResponseRedirect('/')



def cart(request):
    cart_session = request.session.get('cart_session', [])
    count_of_product = len(cart_session)
    products_cart = SneakerCard.objects.filter(id__in=cart_session)
    all_products_sum = 0
    for i in products_cart:
        i.count = cart_session.count(i.id)
        i.sum = i.count * i.price
        all_products_sum += i.sum
        
    return render(request, 'cart.html', {'count_of_product':count_of_product,'products_cart':products_cart, 'all_products_sum': all_products_sum})




def removeCart(request ,id):
    cart_session = request.session.get('cart_session', [])
    carts = []
    carts = cart_session
    carts.remove(id)
    request.session['cart_session'] = carts
    return HttpResponseRedirect('/cart')


def signUp(request):
    if request.method == 'POST':
        user = UserCreationForm(request.POST  )
        if user.is_valid():
            user.save()
            return HttpResponseRedirect('/')
    else:
        user = UserCreationForm()

    return render(request, 'auth.html', {'user':user})

def signin(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            form = AuthenticationForm()
        return render(request, 'auth.html', {'user':form})
    except UnboundLocalError:
        return render(request, 'auth.html')

def signout(request):
    logout(request)
    return HttpResponseRedirect('/')


def order(request):
    cart_session = request.session.get('cart_session', [])
    if request.method == 'POST':
        if len(cart_session) == 0:
            messages.error(request, 'Ваша корзина пустая', extra_tags='danger')
            return redirect('cart')
        else:    
            customer = Customer()
            customer.name = request.POST.get('c_name') 
            customer.last_name = request.POST.get('c_lastname') 
            customer.number = request.POST.get('c_number') 
            customer.addres = request.POST.get('c_addres') 
            customer.message = request.POST.get('c_message') 
            customer.save()
            for i in range(len(cart_session)):
                order = Order()
                cart_session = request.session.get('cart_session', [])
                cart_session_lst = cart_session
                set_list = set(cart_session_lst)
                product_names_and_counts = []
                for i in set_list:
                    product = SneakerCard.objects.get(id = i)
                    product_name = product.title
                    count = cart_session_lst.count(i)
                    products = f"{product_name}-{count}"
                    product_names_and_counts.append(products)
                products_cart = SneakerCard.objects.filter(id__in=cart_session)
                all_products_sum = 0
                for i in products_cart:
                    i.count = cart_session.count(i.id)
                    i.sum = i.count * i.price
                    all_products_sum += i.sum
                order.product = product_names_and_counts
                order.customer = customer
                order.total_price = all_products_sum
                order.phone = customer.number
                order.address = customer.addres
                order.save()
 
            request.session['cart_session'] = []
            messages.error(request, 'Заказ успешно отправлено!',extra_tags='success')
            return redirect('cart')
