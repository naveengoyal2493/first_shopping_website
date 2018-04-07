from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .models import *
from .forms import UserForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import datetime

def home(request):
    return render(request, 'home.html')
# Create your views here.
def view_all_user_orders(request):
    pending_orders = all_orders_table.objects.filter(user_object=request.user).filter(order_delievered=False)
    completed_orders = all_orders_table.objects.filter(user_object=request.user).filter(order_delievered=True)
    return render(request, 'view_all_user_orders.html', {'orders_completed':completed_orders, 'orders_pending':pending_orders})

def user_profile(request, account_id):
    try:
        if int(account_id) == int(request.user.id):
            The_user = User.objects.get(id=account_id)
            add_info = addresses.objects.filter(user=The_user)

            if request.method=="POST":
                update_type = request.POST['change_type']
                print(update_type)
                if update_type == 'pers_details':
                    label = request.POST['label']
                    val = request.POST['val']
                    The_user = check_update_data(label, val, The_user)
                    The_user.save()
                elif update_type == 'addr_details':
                    req_String = request.POST['label']
                    update_val = request.POST['val']
                    check_update_address(req_String, update_val, add_info[0])

            return render(request, 'profile.html', {'user_addresses':add_info, 'user_personal_info':The_user})
        else:
            return HttpResponse('<h1>Invalid Request</h1>')
    except:
        return HttpResponse('<h1>Invalid Request</h1>')

def shopping_cart(request):
    try:
        s_i = shopping_cart_items.objects.filter(user=request.user)
        total_payment = 0;
        for i in s_i:
            total_payment+=i.amount_to_pay
        if request.is_ajax():
            action = request.POST['action']
            if action == 'delete':
                shopping_cart_entry = int(request.POST['entry_id'])
                item = shopping_cart_items.objects.get(pk=shopping_cart_entry)
                item.delete()
            elif action == 'change':
                new_quantity = request.POST['new_quantity']
                print("new_quantity = "+str(new_quantity))
                shopping_cart_entry = int(request.POST['entry_id'])
                item = shopping_cart_items.objects.get(pk=shopping_cart_entry)
                item.quantity = new_quantity
                item.save()

            elif action == 'order':
                all_orders = shopping_cart_items.objects.filter(user=request.user)
                for order in all_orders:
                    order_record = all_orders_table(user_object=request.user, ordered_item =order.product_id, quantity=order.quantity, paying_amount = order.amount_to_pay,order_date=datetime.date.today(), order_delievered=False)
                    order_record.save()
                    order.delete()
        return render(request, 'shopping_cart.html', {'to_order': s_i, 'total_amount':total_payment})
    except:
        return render(request, 'error_pages/shopping_cart.html')
def aboutus(request):
    return render(request, 'about_us.html')

class UserFormView(View):
    form_class = UserForm
    template_name = 'registration_form.html'

    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('products:add_user_address')
        return render(request, self.template_name, {'form:': form})

def add_address(request):

    if request.method=="POST":
        user_object = User.objects.get(id=request.user.id)
        delievery_address = addresses(user=user_object,
        city = request.POST['city'],
        district = request.POST['district'],
        pin = request.POST['pin'],
        state = request.POST['state'],
        area=request.POST['area'],
        house_no = request.POST['house_no'])
        delievery_address.save()
        return redirect(reverse('products:home'))
    return render(request, 'address_first_time.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'login.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/products/1')
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    return render(request, 'login.html')
    #process form data
def check_update_data(req_str, update_value, user_obj):
    if req_str=='first_name':
        user_obj.first_name = update_value
    elif req_str == 'last_name':
        user_obj.last_name = update_value
    elif req_str == 'email':
        user_obj.email = update_value
    return user_obj
def check_update_address(req_str, update_value, addr_obj):
    if req_str=='house_no':
        addr_obj.house_no=str(update_value)
    elif req_str=='pin':
        addr_obj.pin=int(update_value)
    addr_obj.save()
