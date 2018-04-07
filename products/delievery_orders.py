# from django.contrib.auth import User
from .models import *
from .forms import *
from django.shortcuts import render
from django.http import HttpResponse
def view_orders(request):
    if request.user.is_superuser:

        if request.method=="POST":
            customer_id = int(request.POST['user_id'])
            change_orders = all_orders_table.objects.filter(order_delievered=False).filter(user_object=User.objects.get(id=customer_id))
            for i in change_orders:
                i.order_delievered=True
                i.save()

        pending_orders = all_orders_table.objects.filter(order_delievered=False)
        completed_orders = all_orders_table.objects.filter(order_delievered=True)
        users_pending_orders = []
        diff_users = []
        deliever_to = []
        for i in pending_orders:
            if not i.user_object.id in diff_users:
                diff_users.append(i.user_object.id)
                deliever_to.append(addresses.objects.get(user=i.user_object))
        for user_id in diff_users:
            users_pending_orders.append(pending_orders.filter(user_object=User.objects.get(id=user_id)))

        zipped = zip(users_pending_orders, deliever_to)


        return render(request, 'admin_pages/orders.html', {'pending_orders' : zipped, 'deliever_address':deliever_to, 'completed_orders': completed_orders})
    else:
        return HttpResponse('<html><h1>Invalid Request!</h1></html>')
