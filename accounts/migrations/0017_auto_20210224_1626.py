# Generated by Django 3.1.5 on 2021-02-24 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20210222_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(blank=True, max_length=300),
        ),
    ]
