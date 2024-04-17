from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate

from .models import Product, Category
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    product_objects=Product.objects.filter(featured=True,  product_status="published")
    # product_objects=Product.objects.all()

    # item_name = request.GET.get('item_name')
    # if item_name != '' and item_name is not None:
    #     product_objects=product_objects.filter(title__icontains=item_name)

    # paginator=Paginator(product_objects,1)
    # page= request.GET.get('page')
    # product_objects=paginator.get_page(page)

    return render(request,'shop/index.html',{'product_objects':product_objects})

def product_list(request):
    product_objects=Product.objects.filter(product_status="published")
    category_objects=Category.objects.all()

    context={
        'product_objects':product_objects,
        'category_objects':category_objects
    }
    return render(request, 'shop/products.html', context)

def detail(request,id):
    product_object=Product.objects.get(id=id)
    return render(request,'shop/detail.html',{'product_object':product_object})

# def checkout(request):
 
#     if request.method == "POST":
#         items = request.POST.get('items','')
#         name = request.POST.get('name',"")
#         email = request.POST.get('email',"")
#         address = request.POST.get('address',"")
#         city = request.POST.get('city',"")
#         state =request.POST.get('state',"")
#         zipcode = request.POST.get('zipcode',"")
#         total = request.POST.get('total',"")
#         order = Order(items=items,name=name,email=email,address=address,city=city,state=state,zipcode=zipcode,total=total)
#         order.save()
 
#     return render(request,'shop/checkout.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    return render(request,'shop/register.html')