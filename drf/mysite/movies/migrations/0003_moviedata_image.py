# Generated by Django 4.2.8 on 2024-03-05 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_moviedata_cat'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviedata',
            name='image',
            field=models.ImageField(default='Images/None/img.jpg', upload_to='Images/'),
        ),
    ]
