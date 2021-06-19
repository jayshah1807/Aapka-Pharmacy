from django.contrib import admin
from . models import Destination, popular,Profile,product,Item,Transaction,Carts,Comment,Logo, Promo,OrderUpdate,Orders,Category,Type
# Register your models here.
class AdminDestination(admin.ModelAdmin):
    list_display= ['name','image']

class AdminPopular(admin.ModelAdmin):
    list_display= ['name','image']


class AdminProduct(admin.ModelAdmin):
    list_display= ['name','image']


admin.site.register(Logo)
admin.site.register(Carts)
admin.site.register(Comment)
admin.site.register(Promo)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
admin.site.register(Transaction)
admin.site.register(Type)
admin.site.register(Category)
admin.site.register(product,AdminProduct)
admin.site.register(Profile)
admin.site.register(Item)

admin.site.register(Destination,AdminDestination)
admin.site.register(popular,AdminPopular)
# admin.site.register(Payment)
