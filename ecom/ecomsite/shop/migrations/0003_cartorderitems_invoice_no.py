# Generated by Django 4.2.8 on 2024-04-13 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_address_cartorder_cartorderitems_category_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorderitems',
            name='invoice_no',
            field=models.CharField(default=123, max_length=200),
        ),
    ]
