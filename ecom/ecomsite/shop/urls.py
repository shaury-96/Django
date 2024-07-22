from django.urls import path
# from shop.views import index
from shop import views

app_name= 'shop'

urlpatterns=[
    path('',views.index,name='index'),
    path('products/<cid>/',views.product_list,name='product_list'),
    path('product/<pid>/',views.product_detail,name='product_detail'),
    path('products/tag/<tag_slug>/',views.tag_list,name='tag_list'),
    path('ajax_add_review/<pid>/',views.ajax_add_review,name='ajax_add_review'),
    path('product/<pid>/reply/',views.reply_view,name='reply_view'),
    path('product/<pid>/reply_tree/',views.reply_tree,name='reply_tree'),
    path('search/',views.search,name='search'),
    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.cart_page,name='cart-page'),
    path('checkout/',views.checkout_page,name='checkout-page')
]

