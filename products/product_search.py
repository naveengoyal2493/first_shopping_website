from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .models import *
from .forms import UserForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import datetime

class product_search_object:
    def __init__(self):
        self.keyword = [] #will store the product names
        self.synonyms_list = [] # will store lists of synonyms for each product
    def add_to_list(self, prod_obj):
        self.keyword.append(prod_obj.product_name)
        b_list = str(prod_obj.synonyms).split(' ')
        self.synonyms_list.append(b_list)
    def find_word(self, word_name):
        f_res = []
        if word_name in self.keyword:
            return word_name
        else:
            for i in range(len(self.keyword)):
                if word_name in self.synonyms_list[i]:
                    f_res.append(self.keyword[i])
            return f_res
        return None

def search(request):
    search_keyword =  request.GET.get('search_keyword')
    # all_product_names = []
    all_product_types = ["spices", "cereals", "floors", "floor" , "masale", "spice", "dal", "daal", "daals", "cereal", "pulses", "aate", "pulse", "masala", "spice"]
    products_query_set = product.objects.all()

    p_s_o = product_search_object() #reference above specified product_search_object class
    for i in products_query_set:
        p_s_o.add_to_list(i)
    p_l=[]
    filter_response=None
    res = p_s_o.find_word(search_keyword)
    print(res)
    if res:
        if type(res) == list:
            for i in range(len(res)):
                print("res[i] = "+str(res[i]))
                p_l.append(product.objects.filter(product_name=res[i])[0])
        else:
            p_l.append(product.objects.get(product_name=res))
    elif search_keyword in all_product_types:
        search_keyword=search_parameter(search_keyword)
        p_l = product.objects.filter(product_type=search_keyword)
    return render(request, 'products.html', {'products_list': p_l, 'previously_requested':filter_response})


def search_parameter(input_param):
        if input_param=="dal" or input_param=="daal" or input_param=="daals" or input_param=="pulses" or input_param=="pulse":
            return "cereals"
        elif input_param=="masale" or input_param=="spice" or input_param=="masala" or input_param=="spices":
            return "spices"
        # elif input_param=="masale" or input_param=="spice" or input_param=="masala" or input_param=="aate":
