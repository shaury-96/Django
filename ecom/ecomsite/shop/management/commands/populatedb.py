import requests
from django.core.management.base import BaseCommand
from shop.models import Product, Category, Vendor
from userauth.models import CustomUser

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        response = requests.get('https://fakestoreapi.com/products')
        products = response.json()

        for product in products:
            category_name = product['category']
            category=Category.objects.filter(title=category_name).first()
            user=CustomUser.objects.filter(email="admin@gmail.com").first()
            vendor=Vendor.objects.filter(title="Test Vendor 2").first()

            Product.objects.create(
                title=product['title'],
                category=category,
                user=user,
                price=product['price'],
                description=product['description'],
                image=product['image'],
                vendor=vendor,
                product_status="published"

            )

        self.stdout.write(self.style.SUCCESS('Database has been populated with fake data!'))