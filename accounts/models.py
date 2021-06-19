from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from PIL import Image
from django_countries.fields import CountryField
from django.db.models import Sum

class Item(models.Model):
   
   
    product_name = models.CharField(max_length=100, blank=False, default=" ")
    product_price = models.IntegerField(default=None)
    brand_name = models.CharField(max_length=100, blank=False, default=" ")
    product_description = models.TextField(max_length=800, blank=False, null=True)
    available_stock = models.IntegerField(default=0, blank=True, null=False)
    product_frontpage = models.ImageField(default='default.jpg', upload_to='product_frontpages')
    categories = models.ForeignKey('Category',on_delete=models.CASCADE,default=None)
    type_of_item = models.ForeignKey('Type',on_delete=models.CASCADE,default=None)
    product_number = models.CharField(max_length=20,default=None)
    stock = models.IntegerField(default=0)
    def __str__(self):
        return self.product_name + " By " + self.brand_name

class Carts(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Item,
                             on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
   
    ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now=True)
   

    def __str__(self):
        return self.user.username

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.product_price for item in self.Items.all()])

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, default=None)
    profile_image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    contact_no= models.IntegerField(default=None)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()
    
        img = Image.open(self.profile_image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)


class Destination(models.Model) :
    name= models.CharField(max_length=20)
    image= models.ImageField(upload_to='pics')

    @staticmethod
    def get_all_item():
        return Destination.objects.all()


class popular(models.Model) :
    name= models.CharField(max_length=100)
    image= models.ImageField(upload_to='pics')

    @staticmethod
    def get_all_item():
        return popular.objects.all()



class product(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to = 'healthcare_pics')

    @staticmethod
    def get_all_items():
        return product.objects.all()


class Transaction(models.Model):
    token = models.CharField(max_length=120)
    order_id = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp']

class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),

    )
    product = models.ForeignKey(Item, related_name = "reviews" , on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name = "reviews", on_delete=models.CASCADE)
    subject = models.CharField(max_length=20, blank =True)
    comment = models.TextField(max_length=300,blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20,blank=True)
    status = models.CharField(max_length=10,choices=STATUS,default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject + " For " + self.product.product_name

class Promo(models.Model):
    code = models.CharField(max_length=10,blank=True)
    total = models.IntegerField(default=None)
    discount = models.DecimalField(max_digits=7, decimal_places=2,default=None)
    discount_price = models.DecimalField(max_digits=7, decimal_places=2,default=None)
    def __str__(self):
        return self.code

class Orders(models.Model):
    order_id= models.AutoField(primary_key=True)
    amount=models.DecimalField(max_digits=7, decimal_places=2,default=None)
    firstname=models.CharField(max_length=90,default=None)
    lastname=models.CharField(max_length=90,default=None)
    email=models.CharField(max_length=111)
    address=models.CharField(max_length=111)
    country=models.CharField(max_length=111)
    state=models.CharField(max_length=111)
    zip_code=models.CharField(max_length=111)
    items = models.ManyToManyField(Carts,default=None)
    # phone = models.CharField(max_length=111, default="")
    def str(self):
        return self.order_id


class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def str(self):
        return self.update_id


class Category(models.Model):
    category = models.CharField(max_length=30,blank=True,primary_key=True)
    def __str__(self):
        return self.category

class Type(models.Model):
    type_of_item = models.CharField(max_length=30,blank=True, primary_key=True)
    def __str__(self):
        return self.type_of_item

class Logo(models.Model):
    image= models.ImageField(upload_to='logo')


    