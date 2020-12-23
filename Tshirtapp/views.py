from django.shortcuts import render,HttpResponse,redirect
from Tshirtapp.forms.authforms import CustomerCreationForm,AuthForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login as loginUser,logout as logOut
from Tshirtapp.models import *
from math import floor
from django.contrib.auth.decorators import login_required
from Tshirtapp.forms.checkout_form import CheckForm
from instamojo_wrapper import Instamojo
from Tshirt.settings import API_KEY, AUTH_TOKEN
API = Instamojo(api_key=API_KEY,
                auth_token=AUTH_TOKEN,
                endpoint='https://test.instamojo.com/api/1.1/')



def show_product(request,slug):
    tshirt=Tshirt.objects.get(slug=slug)
    size=request.GET.get('size')
    if size is None:
        size=tshirt.sizevarient_set.all().order_by('price').first()
    else:
        size=tshirt.sizevarient_set.get(size=size)
    size_price=floor(size.price)
    sell_price=size_price-(size_price *(tshirt.discount/100))
    sell_price=floor(sell_price)
    return render(request,template_name='Tshirtapp/product_details.html',context={'tshirt':tshirt,'price':size_price,'sell_price':sell_price,'active_size':size})
def home(request):
    tshirt=Tshirt.objects.all()
    print(len(tshirt))

    for t in tshirt:
        all_s=t.sizevarient_set.all().order_by('price') #to get all size '
        print(all_s,'rrrrrrrrrrrrrrrrrrrrrr')
        min_price=t.sizevarient_set.all().order_by('price').first() # to get min price
        print(t, min_price.price, min_price.size)
        t.min_price=min_price.price
        t.after_discount=t.min_price-(t.min_price* t.discount/100)
        t.after_discount=floor(t.after_discount)  #created tags for shortcut in tshirts_tags.py
    context={
        'tshirt':tshirt
    }
    return render(request,template_name='Tshirtapp/home.html',context=context)

def cart(request):

    cart=request.session.get('cart')
    if cart is None:
        cart=[]
    for c in cart:
        tshirt_id=c.get('tshirt')
        tshirt=Tshirt.objects.get(id=tshirt_id)
        c['size']=SizeVarient.objects.get(tshirt=tshirt_id, size=c['size'])
        c['tshirt']=tshirt
        print(cart)
    return render(request,template_name='Tshirtapp/cart.html',context={'cart':cart})

def orders(request):
    user=request.user
    orders=Order.objects.filter(user=user).order_by('-date').exclude(order_status='PENDING')
    context={
          "orders":orders  
        }
    return render(request,template_name='Tshirtapp/order.html',context=context)

def login(request):
    if (request.method=='GET'):
        form=AuthForm
        next_page=request.session.get('next')

        if next_page is not None:
           request.session['next_page']=next_page
        return render(request,template_name='Tshirtapp/login.html',context={'form':form})
    else:
        form=AuthForm(data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user:
                loginUser(request,user)

                session_cart=request.session.get('cart')
                if session_cart is None:
                    session_cart=[]

                else:
                    for c in session_cart:
                        size = c.get('size')
                        tshirt_id = c.get('tshirt')
                        quantity = c.get('quantity')
                        cart_obj = Cart()
                        cart_obj.sizeVarient = SizeVarient.objects.get(
                            size=size, tshirt=tshirt_id)
                        cart_obj.quantity = quantity
                        cart_obj.user = user
                        cart_obj.save()

                cart=Cart.objects.filter(user=user)
                session_cart=[]
                for c in cart:
                    obj={
                        'size':c.sizeVarient.size,
                        'tshirt':c.sizeVarient.tshirt.id,
                        'quantity':c.quantity
                    }
                    session_cart.append(obj)
                request.session['cart']=session_cart
                next_page=request.session.get('next_page')
                if next_page is None:
                    next_page='homepage'
                return redirect(next_page)
        else:

            return render(request,template_name='Tshirtapp/login.html',context={'form':form})

def signup(request):
    if (request.method=='GET'):
        form=CustomerCreationForm()
        context={
            "form":form
        }
        return render(request,template_name='Tshirtapp/signup.html',context=context)
    else:
        form=CustomerCreationForm(request.POST)
        #print(form.is_valid)
        #print(form.errors)
        if form.is_valid():
            user=form.save()
            user.email=user.username
            user.save()
            print(user)
            return render(request,template_name='Tshirtapp/login.html')
        context={
            "form":form
        }
        return render(request,template_name='Tshirtapp/signup.html',context=context)
        

def logout(request):
    #request.session.clear()
    logOut(request)
    return render(request,template_name='Tshirtapp/home.html')


def addtocart(request,slug,size):

    user=None
    if request.user.is_authenticated:
        user=request.user
    cart=request.session.get('cart')
    if cart is None:
        cart=[]

    tshirt=Tshirt.objects.get(slug=slug)
    card_for_anaom_user(cart,size,tshirt)
    
    if user is not None:
        addcarttodatabase(user,size,tshirt)    
        
    request.session['cart']=cart
    return_url=request.GET.get('return_url')
    return redirect(return_url)

def addcarttodatabase(user,size,tshirt):
    size_temp=SizeVarient.objects.get(size=size,tshirt=tshirt)
    existing=Cart.objects.filter(user=user,sizeVarient=size_temp)
    if len(existing)>0:
            obj=existing[0]
            obj.quantity=obj.quantity+1
            obj.save()

    else:
            c=Cart()
            c.user=user
            c.SizeVarient=size
            c.quantity=1
       


def card_for_anaom_user(cart,size,tshirt):
    flag=True
    for cart_obj in cart:
        t_id=cart_obj.get('tshirt')
        s_sort=cart_obj.get('size')
        if t_id==tshirt.id and size==s_sort:
            flag=False
            cart_obj['quantity']=cart_obj['quantity']+1

    if flag:
        cart_obj={
            'tshirt':tshirt.id,
            'size':size,
            'quantity':1
        }
        cart.append(cart_obj)



def cal_total_payable_amount(cart):
    total = 0
    for c in cart:
        discount = c.get('tshirt').discount
        price = c.get('size').price
        sale_price = floor(price - (price * (discount / 100)))
        total_of_single_product = sale_price * c.get('quantity')
        total = total + total_of_single_product

    return total



@login_required(login_url='/login/')
def checkout(request):
    # get Request
    if request.method == 'GET':
        form = CheckForm()
        cart = request.session.get('cart')
        if cart is None:
            cart = []

        for c in cart:
            size_str = c.get('size')
            tshirt_id = c.get('tshirt')
            size_obj = SizeVarient.objects.get(size=size_str, tshirt=tshirt_id)
            c['size'] = size_obj
            c['tshirt'] = size_obj.tshirt

        print(cart)

        return render(request, 'Tshirtapp/checkout.html', {
            "form": form,
            'cart': cart
        })
    else:
        # post request
        form = CheckForm(request.POST)
        user = None
        if request.user.is_authenticated:
            user = request.user
        if form.is_valid():
            cart = request.session.get('cart')
            if cart is None:
                cart = []
            for c in cart:
                size_str = c.get('size')
                tshirt_id = c.get('tshirt')
                size_obj = SizeVarient.objects.get(size=size_str,
                                                   tshirt=tshirt_id)
                c['size'] = size_obj
                c['tshirt'] = size_obj.tshirt
            shipping_address = form.cleaned_data.get('shipping_address')
            phone = form.cleaned_data.get('phone')
            payment_method = form.cleaned_data.get('payment_method')
            total = cal_total_payable_amount(cart)
            print(shipping_address, phone, payment_method, total)
            order = Order()
            order.shipping_address = shipping_address
            order.phone = phone
            order.payment_method = payment_method
            order.total = total
            order.order_status = "PENDING"
            order.user = user
            order.save()
             # saving order items
            for c in cart:
                order_item = OrderItem()
                order_item.order = order
                size = c.get('size')
                tshirt = c.get('tshirt')
                order_item.price = floor(size.price -
                                         (size.price *
                                          (tshirt.discount / 100)))
                order_item.quantity = c.get('quantity')
                order_item.size = size
                order_item.tshirt = tshirt
                order_item.save()
              # crating payment
            response = API.payment_request_create(
                amount=order.total,
                purpose="Payment For Tshirts",
                send_email=False,
                buyer_name=f'{user.first_name} {user.last_name}',
                email=user.email,
                redirect_url="http://localhost:8000/validate_payment")

            payment_request_id = response['payment_request']['id']
            url = response['payment_request']['longurl']

            payment = Payment()
            payment.order = order
            payment.payment_request_id = payment_request_id
            payment.save()
            return redirect(url)
            
        else:
            return redirect('/checkout')
def validatePayment(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    payment_request_id = request.GET.get('payment_request_id')
    payment_id = request.GET.get('payment_id')
    print(payment_request_id, payment_id)
    response = API.payment_request_payment_status(payment_request_id,
                                                  payment_id)
    status = response.get('payment_request').get('payment').get('status')

    if status != "Failed":
        print('Payment Success')
        try:
            payment = Payment.objects.get(
                payment_request_id=payment_request_id)
            payment.payment_id = payment_id
            payment.payment_status = status
            payment.save()

            order = payment.order
            order.order_status = 'PLACED'
            order.save()
            cart = []
            request.session['cart'] = cart
            Cart.objects.filter(user=user).delete()
            return redirect('orders')
        except:
            return render(request, 'Tshirtapp/payment_failed.html')
    else:
        return render(request, 'Tshirtapp/payment_failed.html')

    return HttpResponse("validate Payment")

