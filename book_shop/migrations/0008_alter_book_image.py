# Generated by Django 4.2.1 on 2023-05-28 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_shop', '0007_alter_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products_img'),
        ),
    ]
