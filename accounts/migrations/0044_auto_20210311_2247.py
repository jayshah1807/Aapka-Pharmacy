# Generated by Django 3.1.5 on 2021-03-11 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0043_auto_20210311_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='promo',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=7),
        ),
        migrations.AddField(
            model_name='promo',
            name='total',
            field=models.IntegerField(default=None),
        ),
    ]
