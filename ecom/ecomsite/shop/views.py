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
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.conf import settings
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
    

def help_reply_tree(rid,nodes,visited):

    if rid in visited:
        return
    visited.add(rid)

    replies=ProductReview.objects.filter(parent_review_id=rid)
    parent_user=ProductReview.objects.filter(rid=rid).first().user.first_name
    # print("this is new",parent_user)
    for r in replies:
        node=({
            'id': r.rid,
            'user': r.user.first_name,
            'review': r.review,
            'parent_review_id':rid,
            'parent_user':parent_user
            
        })
        nodes.append(node)
        help_reply_tree(r.rid,nodes,visited)

    return nodes


def reply_tree(request,pid):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rid = data.get('reviewId')
            # reviewUser = data.get('reviewUser')
            # rid = request.POST.get('reviewId')
            print(rid)
            if rid:
                visited=set()
                res = help_reply_tree(rid, [],visited)
                print("here it is", res)
                return JsonResponse({'data': res})
            else:
                return JsonResponse({'error': 'Review ID not provided'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


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

def search(request):
    query=request.GET.get("query")
    products=Product.objects.filter(title__icontains=query).order_by("-date")
    context={
        "product_objects":products,
        "query":query
    }

    return render(request,'shop/products.html',context)


def add_to_cart(request):
    
    item_id = str(request.GET['id'])
    title= request.GET['title']
    qty= int(request.GET['qty'])
    price= float(request.GET['price'])
    total= price * qty
    image= request.GET.get('image','https://picsum.photos/200/300')

    cart_product={
        item_id: {
        'title': title,
        'qty': qty,
        'price': price,
        'total': total,
        'image': image
        }
    }
    
    print(cart_product)
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj']=cart_data

        else:
            cart_data=request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj']=cart_data

    else:
        request.session['cart_data_obj']=cart_product
    
    
    return JsonResponse(
        {
            "data":request.session['cart_data_obj'],
            'totalcartitems':len(request.session['cart_data_obj']),
            
            })


@login_required(login_url='/login/')
def cart_page(request):
    cart_data = request.session.get('cart_data_obj', {})
    total_sum = sum(item['total'] for item in request.session['cart_data_obj'].values())
    context={
        'cart_data': cart_data,
        'totalsum':total_sum
    }
    return render(request, 'shop/cart.html', context)

@login_required
def checkout_page(request):
    host=request.get_host()
    paypal_dict={
        'business':settings.PAYPAL_RECIEVER_MAIL,
        'amount':'200',
        'item_name':'ORD3',
        'invoice':'INV3',
        'currency_code':"USD",
        'notify_url':'http://{}{}'.format(host,reverse("shop:paypal-ipn")),
        'return_url':'http://{}{}'.format(host,reverse("shop:payment-success-page")),
        'cancel_url':'http://{}{}'.format(host,reverse("shop:payment-failed-page")),
    }
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    cart_data = request.session.get('cart_data_obj', {})
    total_sum = sum(item['total'] for item in request.session['cart_data_obj'].values())
    context={
        'cart_data': cart_data,
        'totalsum':total_sum,
        'paypal_payment_button':paypal_payment_button,
    }
    return render(request, 'shop/checkout.html',context)

def payment_success_page(request):
    return render(request,'shop/payment_success.html')

def payment_failed_page(request):
    return render(request, 'shop/payment_failed.html')



    