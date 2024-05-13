from django.db import models
from userauth.models import CustomUser
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


STATUS_CHOICES=(
    ("process","Processing"),
    ("shipped","Shipped"),
    ("deliverd","Delivered"),
)

STATUS=(
    ("draft","Draft"),
    ("disabled","Disabled"),
    ("in_review","In Review"),
    ("rejected","Rejected"),
    ("published","Published")
)

RATING=(
    (1,"⭐☆☆☆☆"),
    (2,"⭐⭐☆☆☆"),
    (3,"⭐⭐⭐☆☆"),
    (4,"⭐⭐⭐⭐☆"),
    (5,"⭐⭐⭐⭐⭐")
)


def user_directory_path(instance,filename):
    return f"user_{instance.user.id}/{filename}"

class Category(models.Model):
    cid=ShortUUIDField(unique=True, length=10, max_length=20, prefix="CAT",alphabet="abcd12345")
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to='category')

    class Meta:
        verbose_name_plural="Categories"

    def category_image(self):
        return mark_safe('<img src="%s" witdth="50" height="50"/>' %(self.image.url))
    
    def __str__(self):
        return self.title

# class Tags(models.Model):
#     pass

class Vendor(models.Model):
    vid= ShortUUIDField(unique=True, length=10,max_length=20,prefix="VEN",alphabet="abcd12345")
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to=user_directory_path)
    description=RichTextUploadingField(null=True, blank=True)
    address=models.CharField(max_length=100, default="some address")
    contact=models.CharField(max_length=12,default="42432")
    vendor_rating=models.CharField(default="10",max_length=10)
    user=models.ForeignKey(CustomUser,on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural="Vendors"
    
    def category_image(self):
        return mark_safe('<img src="%s" witdth="50" height="50"/>' %(self.image.url))
    
    def __str__(self):
        return self.title

class Product(models.Model):
    pid=ShortUUIDField(unique=True, length=10, max_length=20, prefix="PRD",alphabet="abcd12345")
    user=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True)
    title=models.CharField(max_length=100,default='Product title')
    image=models.ImageField(upload_to=user_directory_path)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name='product')
    vendor=models.ForeignKey(Vendor,on_delete=models.SET_NULL,null=True)
    description=RichTextUploadingField(null=True, blank=True)
    price=models.DecimalField(max_digits=99999,decimal_places=2,default="9.99")
    specs=RichTextUploadingField(null=True, blank=True)
    # tags=models.ForeignKey(Tags,on_delete=models.SET_NULL,null=True)
    tags=TaggableManager(blank=True)
    product_status=models.CharField(choices=STATUS,max_length=20,default="in_review")
    status=models.BooleanField(default=True)
    in_stock=models.BooleanField(default=True)
    featured=models.BooleanField(default=False)
    digital=models.BooleanField(default=False)

    sku=ShortUUIDField(unique=True, length=4, max_length=10, prefix="SKU", alphabet="12345")
    date=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(null=True,blank=True)

    class Meta:
        verbose_name_plural="Products"
    
    def product_image(self):
        return mark_safe('<img src="%s" witdth="50" height="50"/>' %(self.image.url))
    
    def __str__(self):
        return self.title

class ProductImages(models.Model):
    images=models.ImageField(upload_to="product-images",default="product.jpg")
    product=models.ForeignKey(Product,related_name="prImages",on_delete=models.SET_NULL,null=True)
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural="Product Images"

class CartOrder(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=99999,decimal_places=2,default="9.99")
    paid_status=models.BooleanField(default=False)
    order_date=models.DateTimeField(auto_now_add=True)
    product_status=models.CharField(choices=STATUS_CHOICES,max_length=30,default="processing")

    class Meta:
        verbose_name_plural="Cart Order"

class CartOrderItems(models.Model):
    order=models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no=models.CharField(max_length=200,default=123)
    product_status=models.CharField(max_length=200)
    item=models.CharField(max_length=200)
    image=models.CharField(max_length=200)
    qty=models.IntegerField(default=0)
    price=models.DecimalField(max_digits=99999,decimal_places=2,default="9.99")
    
    class Meta:
        verbose_name_plural="Cart Order Itmes"
    
    def order_image(self):
        return mark_safe('<img src="/media/%s" witdth="50" height="50"/>' %(self.image))

class ProductReview(models.Model):
    
    rid=ShortUUIDField(unique=True,length=10, max_length=20, prefix="REV",alphabet="abcd12345")
    user=models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,related_name='product_review')
    review=models.TextField()
    rating=models.IntegerField(choices=RATING, default=None, null=True, blank=True)
    date=models.DateTimeField(auto_now_add=True)
    parent_review_id=models.CharField(max_length=20, null=True, default=None)
    

    class Meta:
        verbose_name_plural="Product Reviews"

    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    
class Wishlist(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural="Wishlists"

    def __str__(self):
        return self.product.title

class Address(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True)
    address=models.CharField(max_length=100,null=True)
    status=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural="Address"