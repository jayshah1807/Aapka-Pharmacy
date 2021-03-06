# Generated by Django 3.1.5 on 2021-02-28 06:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0018_cartitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carts',
            name='Items',
        ),
        migrations.AddField(
            model_name='carts',
            name='product',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.item'),
        ),
        migrations.AddField(
            model_name='carts',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='carts',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
