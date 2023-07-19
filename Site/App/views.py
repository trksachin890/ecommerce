from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
from App.models import *
from django.http import JsonResponse
import json


# Create your views here.

def home(request):
    products=Product.objects.all()
    context={'products':products}
    return render(request,'html/home.html',context)

def signin(request):
    if request.method == 'GET':
        return render(request, 'html/login.html')
    elif request.method == 'POST':
        uname = request.POST['username']
        psw = request.POST['password']

        user = authenticate(request, username=uname, password=psw)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')


            


def cart(request, **kwargs):
    
    get_product=Product.objects.get(id=kwargs['id'])
    cart = cart.objects.create(
        name = get_product.name,
        price = get_product.price,
        image = get_product.image,
    )
    cart.save()
    return render(request, 'html/cart.html')
    

def signout(request):
    logout(request)
    return redirect('home')
    

def register(request):
    if request.method=='GET':
        return render (request,'html/register.html')
    else:
        fn=request.POST['firstname']
        ln=request.POST['lastname']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        User.objects.create_user(first_name=fn,last_name=ln,email=email,username=username,password=password)
        return redirect('login')
    

def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        cart, created = cart.objects.get_or_create(user=request.user, completed=False)
        cartitem, created =OrderItem.objects.get_or_create(cart=cart, product=product)
        cartitem.quantity += 1
        cartitem.save()
        
        
        num_of_item = cart.num_of_items
        
        print(cartitem)
    return JsonResponse(num_of_item, safe=False)


def confirm_payment(request, pk):
    cart = cart.objects.get(id=pk)
    cart.completed = True
    cart.save()
    
    return redirect("home")
