from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .models import *
from .forms import UserForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import datetime

def products_list(request, p_n):
    products_list = product.objects.all()
    p_n=1
    total_pages=1
    filter_response=None
    return render(request, 'products_1.html', {'products_list': products_list, 'previously_requested':filter_response, 'no_of_pages':total_pages, 'current_page':p_n})
