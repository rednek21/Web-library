# Generated by Django 4.2.1 on 2023-05-28 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_shop', '0005_alter_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.URLField(blank=True, max_length=2048, null=True),
        ),
    ]
