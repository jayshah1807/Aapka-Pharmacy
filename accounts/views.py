from django.shortcuts import render,redirect
from django.http import HttpResponse ,Http404,HttpResponseRedirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Destination, popular, Profile,product,Item,Transaction,Carts, Comment,Promo,Orders,OrderUpdate
from . forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy,reverse
import json
from django.shortcuts import  get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal as D
from django.db.models import Max
from paytm import Checksum
from django.views.decorators.csrf import csrf_exempt
from accounts.utils import VerifyPaytmResponse
from django.http import HttpResponse
# Create your views here.
MERCHANT_KEY = 'Edbv!fo3jre2Y01R'

res = {}
def home(request):
    dest = Destination.get_all_item()
    pops = popular.get_all_item()
    context = {'dest': dest, 'pops': pops}
    return render(request, 'home.html',context)

    # pops = popular.get_all_item()
    # return render(request, 'home.html',{'pops': pops})

    
def healthcare(request):
    products = product.objects.all()
    return render(request, 'healthcare.html',{'products':products})

def ayush(request):
    products = product.get_all_items()
    return render(request, 'ayush.html',{'products':products})



def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = auth.authenticate(username=username,password=password)

            if user is not None:
                request.session['uid'] = str(user.id)
                request.session.set_expiry(3000)
                print("uid:",request.session["uid"])
                auth.login(request,user)

                return redirect('/')
            else:
                messages.info(request, "Invalid Username or Password")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})
    
    

    

def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request,'Email Taken')
            else :
                user = User.objects.create_user(username=username, email=email, password= password, first_name= first_name, last_name= last_name)
                user.save();
                messages.success(request,'Successfully Account Created')
                return redirect('login')
        else :
             messages.error(request,'Password not matching')
        return redirect('register')
        
    else :
        return render(request, 'register.html')



def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile updated successfully!!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form
        }
    return render(request, 'profile.html', context)

def get_all_items1(request):
    product_list = []
    products1 = []
    if request.method == 'POST':
        
        searchby = request.POST.get('rbtnSearchBy')
        print(searchby)

        if searchby == 'product_name':
            searchkey = request.POST.get('txtSearchName')
            products1 = Item.objects.filter(product_name=searchkey)
            print(searchby)

        if searchby == 'brand_name':
            searchkey = request.POST.get('txtSearchBrand')
            products1 = Item.objects.filter(brand_name=searchkey)
            print(searchby)

        if searchby == 'product_price':
           
            min_price = int(request.POST.get('minPrice'))
            max_price = int(request.POST.get('maxPrice'))
            if not max_price :
                max_price = Item.objects.aggregate(Max('product_price'))
            products1 = Item.objects.filter(product_price__range=[min_price,max_price], type_of_item="Healthcare")
        
        context = {'products1' : products1}
        
        return render(request, "productspage.html", context)

    products1 = Item.objects.filter(type_of_item="Healthcare")
    product_list = list(products1)
    context = {'products1': product_list}
    return render(request, "productspage.html", context)

def productview(request, product_id):
    products2 = Item.objects.filter(id=product_id,type_of_item="Healthcare")
    product = Item.objects.get(id=product_id , type_of_item="Healthcare")
    if request.method == 'POST' and request.user.is_authenticated:
        rate = request.POST.get('rate', 3)
        comment = request.POST.get('comment', '')
        subject = request.POST.get('subject', '')
        user = request.user
        review = Comment.objects.create(product=product, user=request.user, rate=rate, comment=comment , subject=subject)
        print(review)
    
    review  = Comment.objects.filter(product_id = product_id)
    print(review)
    context = {'productdata' : products2[0], 'review':review}
    print(products2)
    return render(request, "products.html", context)

def get_all_aitems(request):
    product_alist = []
    ayproducts = []
    if request.method == 'POST':
        
        asearchby = request.POST.get('SearchBy')
        print(asearchby)

        if asearchby == 'aproduct_name':
            asearchkey = request.POST.get('txtSearchaName')
            print(asearchkey)
            ayproducts = Item.objects.filter(product_name=asearchkey)
            print(asearchby)

        if asearchby == 'abrand_name':
            asearchkey = request.POST.get('txtSearchaBrand')
            ayproducts = Item.objects.filter(brand_name=asearchkey)
            print(asearchby)

        if asearchby == 'product_prices':
            
            min_aprice = int(request.POST.get('minaPrice'))
            max_aprice = int(request.POST.get('maxaPrice'))
            if not max_aprice :
                max_aprice = Item.objects.aggregate(Max('product_price'))
            ayproducts = Item.objects.filter(product_price__range=[min_aprice,max_aprice], type_of_item="Ayurvedic")
    
        aysearchby  = request.POST.get('Category')
        print(aysearchby)

        if aysearchby == 'option1':
            aysearchkey = 'Ayurvedic'
            ayproducts = Item.objects.filter(categories=aysearchkey)
            print(ayproducts)
        
        if aysearchby == 'option2':
            aysearchkey = 'Unani'
            ayproducts = Item.objects.filter(categories=aysearchkey)
            print(ayproducts)
        
        if aysearchby == 'option3':
            aysearchkey = 'Siddha'
            ayproducts = Item.objects.filter(categories=aysearchkey)
            print(ayproducts)

        

        context = {'ayproducts' : ayproducts}
        
        return render(request, "ayush.html", context)

    ayproducts = Item.objects.filter(type_of_item = "Ayurvedic")
    product_alist = list(ayproducts)
    context = {'ayproducts': product_alist}
    return render(request, "ayush.html", context)

def aproductview(request, product_id):
    aproducts = Item.objects.filter(id=product_id,type_of_item = "Ayurvedic")
    product = Item.objects.get(id=product_id , type_of_item="Ayurvedic")
    if request.method == 'POST' and request.user.is_authenticated:
        rate = request.POST.get('rate', 3)
        comment = request.POST.get('comment', '')
        subject = request.POST.get('subject', '')
        user = request.user
        review = Comment.objects.create(product=product, user=request.user, rate=rate, comment=comment , subject=subject)
        print(review)
    
    review  = Comment.objects.filter(product_id = product_id)
    print(review)
    
    context = {'aproduct' : aproducts[0], 'review':review}
    print(aproducts)
    return render(request, "aproducts.html", context)

def get_all_hitems(request):
    product_hlist = []
    hoproducts = []
    if request.method == 'POST':
        
        asearchby = request.POST.get('SearchBy')
        print(asearchby)

        if asearchby == 'aproduct_name':
            asearchkey = request.POST.get('txtSearchaName')
            print(asearchkey)
            ayproducts = Item.objects.filter(product_name=asearchkey)
            print(asearchby)

        if asearchby == 'abrand_name':
            asearchkey = request.POST.get('txtSearchaBrand')
            ayproducts = Item.objects.filter(brand_name=asearchkey)
            print(asearchby)

        if asearchby == 'product_price':
            # if 'minPrice' in request.POST:
            min_price = int(request.POST.get('minPrice'))
            max_price = int(request.POST.get('maxPrice'))
            if not max_price :
                max_price = Item.objects.aggregate(Max('product_price'))
            ayproducts = Item.objects.filter(product_price__range=[min_price,max_price])
    
        aysearchby  = request.POST.get('Category')
        print(aysearchby)

        if aysearchby == 'option1':
            aysearchkey = 'Children'
            hoproducts = Item.objects.filter(categories=aysearchkey)
            print(hoproducts)
        
        if aysearchby == 'option2':
            aysearchkey = 'Teenage'
            hoproducts = Item.objects.filter(categories=aysearchkey)
            print(hoproducts)
        
        if aysearchby == 'option3':
            aysearchkey = 'Adult'
            hoproducts = Item.objects.filter(categories=aysearchkey)
            print(hoproducts)

        if aysearchby == 'option4':
            aysearchkey = 'Oldage'
            hoproducts = Item.objects.filter(categories=aysearchkey)
            print(hoproducts)


        

        context = {'hoproducts' : hoproducts}
        
        return render(request, "homeo.html", context)

    hoproducts = Item.objects.filter(type_of_item = "Homeopathy")
    product_hlist = list(hoproducts)
    context = {'hoproducts': product_hlist}
    return render(request, "homeo.html", context)

def hproductview(request, product_id):
    hproducts = Item.objects.filter(id=product_id,type_of_item = "Homeopathy")
    product = Item.objects.get(id=product_id , type_of_item="Homeopathy")
    if request.method == 'POST' and request.user.is_authenticated:
        rate = request.POST.get('rate', 3)
        comment = request.POST.get('comment', '')
        subject = request.POST.get('subject', '')
        user = request.user
        review = Comment.objects.create(product=product, user=request.user, rate=rate, comment=comment , subject=subject)
        print(review)
    
    review  = Comment.objects.filter(product_id = product_id)
    print(review)
    
    context = {'hproduct' : hproducts[0], 'review':review}
    print(hproducts)
    return render(request, "hproduct.html", context)


def search(request):
    if request.method == 'GET':

        search=request.GET.get('search')
        products1=Item.objects.filter(product_name=search) 
        params={'products1':products1}
        
        return render(request, 'search.html', params)

def asearch(request):
    if request.method == 'GET':

        search=request.GET.get('search')
        bsearch=request.GET.get('search')
        ayproducts=Item.objects.filter(product_name=search) 
        params={'ayproducts':ayproducts}
        
        return render(request, 'search.html', params)

def cart(request):
    user = int(request.session['uid'])
    cart = Carts.objects.filter(user = user)
    items = {}
    if cart:
        for c in cart:
            print("cart:",c)
            product_id = c.product_id
            Items = Item.objects.get(id=product_id)
            items[c]=Items
        print(cart,items)
    context={'item':items}
    return render(request, 'cart.html',context)


@login_required()
def add_to_cart(request, product_id):
    user = int(request.session["uid"])
    products2 = Item.objects.filter(id=product_id)
    cart = Carts.objects.filter(user=user,product=product_id)
    print(cart)
    if len(cart)>0:
        print(cart)
        for c in cart:
            c.quantity += 1
            c.save()
            print(cart)
    else:
        c = Carts()
        c.product_id = product_id
        c.user_id = user
        c.save()
    context = {'productdata' : products2[0]}
    return render(request,"products.html", context)

@login_required()
def addTocart(request, product_id):
    user = int(request.session["uid"])
    aproducts = Item.objects.filter(id=product_id,type_of_item="Ayurvedic")
    cart = Carts.objects.filter(user=user,product=product_id)
    print(cart)
    if len(cart)>0:
        print(cart)
        for c in cart:
            c.quantity += 1
            c.save()
            print(cart)
    else:
        c = Carts()
        c.product_id = product_id
        c.user_id = user
        c.save()
    context = {'aproduct' : aproducts[0]}
    return render(request,"aproducts.html",context)

@login_required()
def addtocart(request, product_id):
    user = int(request.session["uid"])
    hproducts = Item.objects.filter(id=product_id,type_of_item="Homeopathy")
    cart = Carts.objects.filter(user=user,product=product_id)
    print(cart)
    if len(cart)>0:
        print(cart)
        for c in cart:
            c.quantity += 1
            c.save()
            print(cart)
    else:
        c = Carts()
        c.product_id = product_id
        c.user_id = user
        c.save()
    context = {'hproduct' : hproducts[0]}
    return render(request,"hproduct.html",context)


def checkout(request,total):
    # dest = Destination.get_all_item()
    

    if request.method=="POST":
    
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        amount = total
        email = request.POST.get('email', '')
        address = request.POST.get('address', '') + " " + request.POST.get('address2', '')
        # city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip', '')
        country = request.POST.get('country', '')

        order = Orders(firstname=firstname,lastname=lastname, email=email, address= address, state=state, zip_code=zip_code, country=country, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()

        thank=True
        request.session['oid'] = str(order.order_id)
        request.session.set_expiry(3000)
        id = order.order_id
        # return render(request, 'checkout.html', {'thank':thank, 'id':id})
        #request paytm to transfer the amount to your account after payment by user
        param_dict={

                'MID': 'CokjuX79375453320495',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': amount,
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return  render(request, 'payment.html', {'param_dict': param_dict})
        
    # return render(request, 'checkout.html')

    user = int(request.session['uid'])
    cart = Carts.objects.filter(user = user)
    items = {}
    if cart:
        for c in cart:
            print("cart:",c)
            product_id = c.product_id
            Items = Item.objects.get(id=product_id)
            items[c]=Items
        print(cart,items)
    context={'item':items,'total':total}

    return render(request, 'checkout.html',context)

# def payment(request):
#     if request.method=="POST":
#         items_json = request.POST.get('itemsJson', '')
#         name = request.POST.get('name', '')
#         amount = request.POST.get('amount', '')
#         email = request.POST.get('email', '')
#         address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
#         city = request.POST.get('city', '')
#         state = request.POST.get('state', '')
#         zip_code = request.POST.get('zip_code', '')
#         phone = request.POST.get('phone', '')

#         order = Orders(items_json= items_json, name=name, email=email, address= address, city=city, state=state, zip_code=zip_code, phone=phone, amount=amount)
#         order.save()
#         update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
#         update.save()

#         thank=True
#         id = order.order_id
#         # return render(request, 'checkout.html', {'thank':thank, 'id':id})
#         #request paytm to transfer the amount to your account after payment by user
#         param_dict={

#                 'MID': 'jIxOuT44108029771814',
#                 'ORDER_ID': str(order.order_id),
#                 'TXN_AMOUNT': amount,
#                 'CUST_ID': email,
#                 'INDUSTRY_TYPE_ID': 'Retail',
#                 'WEBSITE': 'WEBSTAGING',
#                 'CHANNEL_ID': 'WEB',
#                 'CALLBACK_URL':'http://127.0.0.1:8080/handlerequest/',

#         }
#         param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
#         return  render(request, 'paytm.html', {'param_dict': param_dict})
        
#     return render(request, 'checkout.html')


# @csrf_exempt
# def response(request):
#     resp = VerifyPaytmResponse(request)
#     if resp['verified']:
#         # save success details to db; details in resp['paytm']
#         return HttpResponse("<center><h1>Transaction Successful</h1><center>", status=200)
#     else:
#         # check what happened; details in resp['paytm']
#         return HttpResponse("<center><h1>Transaction Failed</h1><center>", status=400)


@csrf_exempt
def handlerequest(request):
    uid = request.user.id
    oid = request.session.get('oid')
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            global res
            res = response_dict
            return redirect('/success/')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})

def success(request):
    global res
    print(res)
    uid = int(request.session['uid'])
    oid = int(request.session['oid'])
    print(uid,oid)
    print('order successful')
    cart = Carts.objects.filter(user_id = uid)
    order = Orders.objects.filter(order_id=oid)        
    for o in order:
        for c in cart:
            print(c.product_id)
            item = list(Item.objects.filter(id = c.product_id))
            for i in item:
                i.available_stock -= c.quantity
                i.save()
            # item.stock -= c.quantity
            # item.save()
            o.items.add(c)
        o.save()
    return render(request, 'paymentstatus.html', {'response':res})

def increment(request,product_id):
    uid = request.session['uid']
    cart = Carts.objects.filter(user_id=uid,product_id = product_id)
    print(cart)
    for c in cart:
        item = Item.objects.filter(id = product_id)
        for i in item:
            if i.available_stock != c.quantity:
                c.quantity += 1
                c.save()
            else:
                messages.error(request,"Can't add further items")
    return redirect('/cart/')

def decrement(request,product_id):
    uid = request.session['uid']
    cart = Carts.objects.filter(user_id=uid,product_id = product_id)
    print(cart)
    for c in cart:
        if c.quantity == 1:
            c.delete()
        else:
            c.quantity -= 1
            c.save()
    return redirect('/cart/')

def promocode(request,total):
    pcode = request.POST['code']
    print(pcode)
    code = Promo.objects.filter(code=pcode)
    for c in code:
        discount = c.discount
        total = float(total) * float(discount)
        price = float(total) / float(discount)
        discount_price = c.discount_price
        dis = float(discount_price) * float(price)
    print(total)
    return redirect('/checkout/'+str(total)+'/')


def view_order(request):
    user = int(request.session['uid'])
    cart = Carts.objects.filter(user = user)
    orders = []
    for c in cart:
        myorders = Orders.objects.filter(items=c)
        if myorders:
            for o in myorders:
                for i in o.items.all():
                    d = {}
                    d['oid']=o.order_id
                    d['pname']= i.product.product_name
                    d['quantity'] = i.quantity
                    d['img']= i.product.product_frontpage.url
                    d['price'] = i.product.product_price
                    d['state'] = o.state
                    d['zip_code'] = o.zip_code
                    d['address'] = o.address
                    orders.append(d)
            break
    print(orders)
    context={'orders':orders}
    return render(request,'orders.html',context)



# def add_to_cart(request, product_id):

#     user = None
#     if request.user.is_authenticated:
#         user = request.user

#     cart = request.session.get('cart')

#     if cart is None:
#         cart = []

#     Items = Item.objects.get(id=product_id)
    

#     flag = True
#     for cart_obj in cart:
#         product_id = cart_obj.get('Item')
        
#         if product_id == product.id:
#             flag = False
#             cart_obj['quantity'] = cart_obj['quantity'] + 1
#     if flag:
#         cart_obj = {
#             'Item': product.id,
#             'quantity': 1
            
#         }
#         cart.append(cart_obj)

#     if user is not None:
#         existing = Carts.objects.filter(product=product_id, user=user)
#         if len(existing) > 0:
#             obj = existing[0]

#             obj.quantity = obj.quantity+1
#             obj.save()

#         else:
#             c = Carts()
#             c.product = Items
#             c.user = user
#             c.quantity = 1
#             c.save()

#     request.session['cart'] = cart
#     return_url = request.GET.get('return_url')
#     cart = request.session.get('cart')
#     print(cart)
#     return redirect(return_url)
    # uid = request.session['uid']
    # cart = CartItem.objects.raw("Select * from accounts_cartitem where user_id =" +str(uid)+ " && product_id ="+str(product_id)+";" )
    # if len(list(cart)) != 0:
    #     cart.quantity += 1
    #     carts = Carts.objects.filter(Q(user=request.session["uid"]) & Q(Items=product_id))
    # else:
    #     newCartItem = CartItem()
    #     newCartItem.user_id = request.session["uid"]
    #     newCartItem.product_id = product_id
    #     newCartItem.save()
    #     newCart  = Carts()
    #     # s = list(newCartItem)

        
    #     newCart.user_id = request.session["uid"]
    #     newCart.Items.add(newCartItem)
    #     newCart.save()
    # products2 = Item.objects.filter(id=product_id)
    # context = {'productdata' : products2[0]}
    # print(products2)
    # return render(request, "products.html", context)
    # for cart_obj in cart:
    #     product_id = cart_obj.get('Item')
    #     if product_id == product.id:
    # #         flag = False
    #         cart_obj['quantity'] = cart_obj['quantity'] + 1
    # existing = CartItem.objects.filter(product=product, id=user.id)
    # if len(existing) > 0:
    #     obj = existing[0]

    #     obj.quantity = obj.quantity+1
    #     obj.save()
    # # create order associated with thproduct = Item.objects.get(id=product_id)
    # # check if the user already owns this product
    # # if product in request.user.profile.products.all():
    #     # messages.info(request, 'You already own this ebook')
    #     # return redirect(reverse('products')) 
    # # create orderItem of the selected product
    # cart = request.session.get('cart')
    # order_item = CartItem.objects.get_or_create(product=product)
    # user_order= Carts.objects.get_or_create(user=request.user,ordered=False)
    # user_order.product.add(order_item)
    # messages.info(request, "Item added to cart")
    
    # flag = True
    # for cart_obj in cart:
    #     product_id = cart_obj.get('Item')
    #     # cat_temp = cart_obj.get('category')
    #     if product_id == product.id:
    #         flag = False
    #         cart_obj['quantity'] = cart_obj['quantity'] + 1
    # if flag:
    #     cart_obj = {
    #         'Item': product.id,
    #         'quantity': 1
    #         # 'category': category
    #     }
    #     cart.append(cart_obj)
    # if len(existing) > 0:
    #     obj = existing[0]

    #     obj.quantity = obj.quantity+1
    #     obj.save()

    # else:
    #     c = CartItem()
    #     c.user = user
    #     c.product = product
    #         # c.Category = cat_temp
    #     c.quantity = 1
    #         # c.save()
    # # if status:
    # #     # generate a reference code
    # #     user_order.ref_code = generate_order_id()
    # #     user_order.save()

    # # show confirmation message and redirect back to the same page
    # messages.info(request, "Item added to cart")
    # user = None
    # if request.user.is_authenticated:
    #     user = request.user

    # cart = request.session.get('cart')
    # # cart = Cart.objects.filter(user__id = request.user.id)
    # if cart is None:
    #     cart = []

    # Items = Item.objects.get(id=product_id)
    # cat_temp = Category.objects.get(name=category)

    # flag = True
    # for cart_obj in cart:
    #     product_id = cart_obj.get('Item')
    #     # cat_temp = cart_obj.get('category')
    #     if product_id == product.id:
    #         flag = False
    #         cart_obj['quantity'] = cart_obj['quantity'] + 1
    # if flag:
    #     cart_obj = {
    #         'Item': product.id,
    #         'quantity': 1
    #         # 'category': category
    #     }
    #     cart.append(cart_obj)

    # if user is not None:
    #     existing = CartItem.objects.filter(product=product, id=user.id)
    #     if len(existing) > 0:
    #         obj = existing[0]

    #         obj.quantity = obj.quantity+1
    #         obj.save()

    #     else:
    #         c = CartItem()
    #         c.user = user
    #         c.product = product
    #         # c.Category = cat_temp
    #         c.quantity = 1
    #         # c.save()

    # request.session['cart'] = cart
    # return_url = request.GET.get('return_url')
    # cart = request.session.get('cart')
    # print(cart)
    # return redirect(return_url)





# def addcomment(request, product_id):
#     if request.user.is_authenticated:
#         product = Item.objects.get(id=product_id)
#         if request.method == 'POST':
#             form = CommentForm(request.POST)
#             if form.is_valid():
#                 data = form.save(commit=False)
#                 data.comment = comment
#                 data.subject = subject
#                 data.rate = rate
#                 data.user = user
#                 data.product = product
#                 data.save()
#                 return HttpResponseRedirect(reverse('addcomment', args=[product_id]))
#         else:
#             form = CommentForm()
#         template = loader.get_template('products.html')
#         context = {
#             'form': form,
#             'product': product
#         }
#         return HttpResponse(template.render(context,request))
    
        
    # if request.method == 'POST':
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         data = Comment()
    #         # data.name = form.cleaned_data['name']
    #         data.subject = form.cleaned_data['subject']
    #         data.comment = form.cleaned_data['comment']
    #         data.ip = request.Meta.get('REMOTE_ADDR')
    #         data.product_id = id
    #         current_user = request.user
    #         data.user__id = current_user.id
    #         data.save()
    #         messages.success(request, "Your review has been sent, Thank you for your Interest")
    #         return HttpResponseRedirect(url)
    # return HttpResponseRedirect(url)



# @login_required()
# def order_details(request, **kwargs):
#     existing_order = get_user_pending_order(request)
#     context = {
#         'order': existing_order
#     }
#     return render(request, 'cart.html', context)

# def add_to_cart(request, product_id):

#     user = None
#     if request.user.is_authenticated:
#         user = request.user

#     cart = request.session.get('cart')
#     # cart = Cart.objects.filter(user__id = request.user.id)
#     if cart is None:
#         cart = []

#     Items = Item.objects.get(id=product_id)
#     # cat_temp = Category.objects.get(name=category)

#     flag = True
#     for cart_obj in cart:
#         product_id = cart_obj.get('Item')
#         # cat_temp = cart_obj.get('category')
#         if product_id == Items.id:
#             flag = False
#             cart_obj['quantity'] = cart_obj['quantity'] + 1
#     if flag:
#         cart_obj = {
#             'Item': Items.id,
#             'quantity': 1
#             # 'category': category
#         }
#         cart.append(cart_obj)

#     if user is not None:
#         existing = Cart.objects.filter(Items=Items, user=user)
#         if len(existing) > 0:
#             obj = existing[0]

#             obj.quantity = obj.quantity+1
#             obj.save()

#         else:
#             c = Cart()
#             c.user = user
#             c.Items = Items
#             # c.Category = cat_temp
#             c.quantity = 1
#             c.save()

#     request.session['cart'] = cart
#     return_url = request.GET.get('return_url')
#     cart = request.session.get('cart')
#     print(cart)
#     return redirect(return_url)

# class OrderSummaryView(LoginRequiredMixin, View):
#     def get(self, *args, **kwargs):
#         try:
#             order = Order.objects.get(user=self.request.user, ordered=False)
#             context = {
#                 'object': order
#             }
#             return render(self.request, 'order_summary.html', context)
#         except ObjectDoesNotExist:
#             messages.warning(self.request, "You do not have an active order")
#             return redirect("/")


# class ItemDetailView(DetailView):
#     model = Item
#     template_name = "products.html"



# @login_required
# def add_to_cart(request, slug):
#     item = get_object_or_404(Item, slug=slug)
#     order_item, created = cart.objects.get_or_create(
#         item=item,
#         user=request.user,
#         ordered=False
#     )
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.items.filter(item__slug=item.slug).exists():
#             order_item.quantity += 1
#             order_item.save()
#             messages.info(request, "This item quantity was updated.")
#             return redirect("core:order-summary")
#         else:
#             order.items.add(order_item)
#             messages.info(request, "This item was added to your cart.")
#             return redirect("core:order-summary")
#     else:
#         ordered_date = timezone.now()
#         order = Order.objects.create(
#             user=request.user, ordered_date=ordered_date)
#         order.items.add(order_item)
#         messages.info(request, "This item was added to your cart.")
#         return redirect("core:order-summary")


# @login_required
# def remove_from_cart(request, slug):
#     item = get_object_or_404(Item, slug=slug)
#     order_qs = Order.objects.filter(
#         user=request.user,
#         ordered=False
#     )
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.items.filter(item__slug=item.slug).exists():
#             order_item = cart.objects.filter(
#                 item=item,
#                 user=request.user,
#                 ordered=False
#             )[0]
#             order.items.remove(order_item)
#             order_item.delete()
#             messages.info(request, "This item was removed from your cart.")
#             return redirect("core:order-summary")
#         else:
#             messages.info(request, "This item was not in your cart")
#             return redirect("core:product", slug=slug)
#     else:
#         messages.info(request, "You do not have an active order")
#         return redirect("core:product", slug=slug)


# @login_required
# def remove_single_item_from_cart(request, slug):
#     item = get_object_or_404(Item, slug=slug)
#     order_qs = Order.objects.filter(
#         user=request.user,
#         ordered=False
#     )
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.items.filter(item__slug=item.slug).exists():
#             order_item = cart.objects.filter(
#                 item=item,
#                 user=request.user,
#                 ordered=False
#             )[0]
#             if order_item.quantity > 1:
#                 order_item.quantity -= 1
#                 order_item.save()
#             else:
#                 order.items.remove(order_item)
#             messages.info(request, "This item quantity was updated.")
#             return redirect("core:order-summary")
#         else:
#             messages.info(request, "This item was not in your cart")
#             return redirect("core:product", slug=slug)
#     else:
#         messages.info(request, "You do not have an active order")
#         return redirect("core:product", slug=slug)

    