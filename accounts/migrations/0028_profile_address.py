# Generated by Django 3.1.5 on 2021-03-04 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.TextField(max_length=500, null=True),
        ),
    ]
