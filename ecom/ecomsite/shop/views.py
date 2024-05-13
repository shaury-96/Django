from django.shortcuts import render, redirect, get_object_or_404
from taggit.models import Tag
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.db.models import Avg
from .models import Product, Category, ProductReview
from django.core.paginator import Paginator
from django import template
from .forms import ProductReviewForm
from django.http import JsonResponse
from django.utils.dateformat import DateFormat
import json
# from django.db.models.query import QuerySets



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

def product_list(request,cid):

    category_objects=Category.objects.all()
    product_objects=Product.objects.filter(product_status="published")
    selected_category = None

    if cid!="all": 
        category_objects=Category.objects.get(cid=cid)
        # print(type(category_objects))
        product_objects=Product.objects.filter(product_status="published",category=category_objects)
        category_objects=Category.objects.all()
        # category_objects=[].append(category_objects)
        # queryset = QuerySet(model=None)
        # category_objects=Category.objects.filter(cid=cid)
    
    # print(type(product_objects), category_objects)

    context={
        'product_objects':product_objects,
        'category_objects':category_objects,
        'selected_category':cid
    }
    return render(request, 'shop/products.html', context)



def product_detail(request,pid):
    product_object=Product.objects.get(pid=pid)
    prImages=product_object.prImages.all()
    rProducts=Product.objects.filter(category=product_object.category, product_status="published").exclude(pid=product_object.pid)[:3]
    reviews=ProductReview.objects.filter(product=product_object).order_by('-date')
    avg_rating=reviews.aggregate(rating=Avg('rating'))
    review_form=ProductReviewForm()

    context={
        'product_object':product_object,
        'prImages':prImages,
        'rProducts':rProducts,
        'reviews':reviews,
        'avg_rating':avg_rating,
        'review_form':review_form
    }
    return render(request,'shop/product_detail.html',context)





def tag_list(request,tag_slug=None):
    products=Product.objects.filter(product_status="published")
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag, slug=tag_slug)
        products=products.filter(tags__in=[tag])
    
    context={
        'products':products,
        'tag':tag
    }
    return render(request,'shop/tag_page.html',context)


def ajax_add_review(request, pid):
    product=Product.objects.get(pk=pid)
    user=request.user

    review=ProductReview.objects.create(
        user=user,
        product=product,
        rating=request.POST.get('rating'),
        review=request.POST.get('review')
    )

    avg_reviews_rating=ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    context={
        'user': {
            'id': user.id,
            'username': user.first_name,
        },
        'product':product.id,
        'rating':request.POST.get('rating'),
        'review':request.POST.get('review'),
        'date':DateFormat(review.date).format('d M, Y'),
        'avg_reviews_rating':avg_reviews_rating
    }

    
    
    return JsonResponse(
        {
            'bool':True,
            'context':context
        }
    )

def reply_view(request,pid):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        # print(data.get('productId'))
        review_id = data.get('reviewId')
        reply_text=data.get('replyText')
        product=Product.objects.filter(pid=pid).first()
        user=request.user
        # Process the review ID and logged-in user data as needed
        # Implement your reply submission logic here
        print(ProductReview.objects.filter(rid=review_id))
        print(review_id)
        review=ProductReview.objects.create(
            user=user,
            product=product,
            review=reply_text,
            parent_review_id=ProductReview.objects.filter(rid=review_id).first().rid
        )


        return JsonResponse({'message': 'Reply submitted successfully!'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    


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

