# Generated by Django 3.1.5 on 2021-03-02 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_ayurvedic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ayurvedic',
            name='product_frontpage',
            field=models.ImageField(default='default.jpg', upload_to='ayurvedic_frontpages'),
        ),
    ]
