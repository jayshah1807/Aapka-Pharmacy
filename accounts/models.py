from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from PIL import Image
from django_countries.fields import CountryField
from django.db.models import Sum
# from django import forms
# class Member(AbstractUser):
#     contact_no = models.CharField(max_length=10, validators=[
#         RegexValidator(regex='^.{10}$', message='Contact number must be of length 10', code='nomatch')])

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Logo(models.Model):
    image= models.ImageField(upload_to='logo')


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

# class Profiles(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # address = models.CharField(max_length=500)
#     date_of_birth = models.DateField(null=True, default=None)
#     profile_image = models.ImageField(default='default.jpg', upload_to='profile_pics')
#     contact_no= models.IntegerField(default=None)
#     is_complete = models.BooleanField(default=False)

#     def __str__(self):
#         return f'{self.user.username} Profile'

#     def save(self):
#         super().save()
    
#         img = Image.open(self.profile_image.path)
#         if img.height > 300 or img.width > 300:
#             output_size = (300,300)
#             img.thumbnail(output_size)
#             img.save(self.profile_image.path)


# Create your models here.
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

# class healthcare(models.Model) :
#     name= models.CharField(max_length=20, default="")
#     img= models.ImageField(upload_to='healthcare_pics')

#     @staticmethod
#     def get_all_items():
#         return healthcare.objects.all()

class product(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to = 'healthcare_pics')

    @staticmethod
    def get_all_items():
        return product.objects.all()




class Item(models.Model):
   
    # book_id = models.AutoField()
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


# class Ayurvedic(models.Model):
   
#     # book_id = models.AutoField()
#     product_name = models.CharField(max_length=100, blank=False, default=" ")
#     product_price = models.IntegerField(default=None)
#     brand_name = models.CharField(max_length=100, blank=False, default=" ")
#     product_description = models.TextField(max_length=500, blank=False, null=True)
#     available_stock = models.IntegerField(default=0, blank=True, null=False)
#     product_frontpage = models.ImageField(default='default.jpg', upload_to='ayurvedic_frontpages')
#     categories = models.CharField(max_length=30,default=" ")
#     product_number = models.CharField(max_length=20,default=" ")
   
#     def __str__(self):
#         return self.product_name + " By " + self.brand_name


    
    # def slug(self):
    #     return slugify(self.id)

# class CartItem(models.Model):
#     user = models.ForeignKey(User,
#                              on_delete=models.CASCADE, default="")
#     product = models.OneToOneField(Item, on_delete=models.SET_NULL, null=True)
#     quantity = models.IntegerField(default=1)
#     def __str__(self):
#         return self.product.product_name


class Carts(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Item,
                             on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    # check_medicine = models.IntegerField() #1 health,2 ayurvedic,3 homeopathic
    ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now=True)
    # item = models.ForeignKey(Item, on_delete=models.CASCADE)
    
    # product_frontpage = models.ImageField()
    # def __str__(self):
        # return self.Items.product_name

    def __str__(self):
        return self.user.username

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.product_price for item in self.Items.all()])

# class OrderProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     products = models.ManyToManyField(Item, blank=True)
    

#     def __str__(self):
#         return self.user.username

class Transaction(models.Model):
    # profile = models.ForeignKey(OrderProfile, on_delete=models.CASCADE)
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




    # def get_total_item_price(self):
    #     return self.quantity * self.item.price

    # def get_total_discount_item_price(self):
    #     return self.quantity * self.item.discount_price

    # def get_amount_saved(self):
    #     return self.get_total_item_price() - self.get_total_discount_item_price()

    # def get_final_price(self):
    #     if self.item.discount_price:
    #         return self.get_total_discount_item_price()
    #     return self.get_total_item_price()

# class Order(models.Model):
#     user = models.ForeignKey(User,
#                              on_delete=models.CASCADE)
#     ref_code = models.CharField(max_length=20, blank=True, null=True)
#     items = models.ManyToManyField(OrderItems)
#     start_date = models.DateTimeField(auto_now_add=True)
#     ordered_date = models.DateTimeField()
#     ordered = models.BooleanField(default=False)
#     # shipping_address = models.ForeignKey(
#     #     'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
#     # billing_address = models.ForeignKey(
#     #     'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
#     # payment = models.ForeignKey(
#     #     'Payment', on_delete=models.SET_NULL, blank=True, null=True)
#     # coupon = models.ForeignKey(
#     #     'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
#     # being_delivered = models.BooleanField(default=False)
#     # received = models.BooleanField(default=False)
#     # refund_requested = models.BooleanField(default=False)
#     # refund_granted = models.BooleanField(default=False)

    

#     def __str__(self):
#         return self.user.username

#     def get_total(self):
#         total = 0
#         for order_item in self.items.all():
#             total += order_item.get_final_price()
#         if self.coupon:
#             total -= self.coupon.amount
#         return total


# class Address(models.Model):
#     user = models.ForeignKey(User,
#                              on_delete=models.CASCADE)
#     street_address = models.CharField(max_length=100)
#     apartment_address = models.CharField(max_length=100)
#     country = CountryField(multiple=False)
#     zip = models.CharField(max_length=100)
#     address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
#     default = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.username

#     class Meta:
#         verbose_name_plural = 'Addresses'


# class Payment(models.Model):
#     stripe_charge_id = models.CharField(max_length=50)
#     user = models.ForeignKey(User,
#                              on_delete=models.SET_NULL, blank=True, null=True)
#     amount = models.FloatField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username


# class Coupon(models.Model):
#     code = models.CharField(max_length=15)
#     amount = models.FloatField()

#     def __str__(self):
#         return self.code


# class Refund(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     reason = models.TextField()
#     accepted = models.BooleanField(default=False)
#     email = models.EmailField()

#     def __str__(self):
#         return f"{self.pk}"


# def userprofile_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         userprofile = UserProfile.objects.create(user=instance)


# post_save.connect(userprofile_receiver, sender=User)