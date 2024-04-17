from django.contrib import admin
from .models import Product, Category, CartOrder, Vendor, CartOrderItems, ProductImages, ProductReview, Wishlist, Address


# Register your models here.
class ProductImagesAdmin(admin.TabularInline):
    model=ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines=[ProductImagesAdmin]
    list_display=['user','title','product_image']


admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(CartOrder)
admin.site.register(Vendor)
admin.site.register(CartOrderItems)

admin.site.register(ProductReview)
admin.site.register(Wishlist)
admin.site.register(Address)