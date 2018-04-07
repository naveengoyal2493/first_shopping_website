from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .models import *
from .forms import UserForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import datetime
import json

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

def search_parameter(input_param):
        if input_param=="dal" or input_param=="daal" or input_param=="daals" or input_param=="pulses" or input_param=="pulse":
            return "cereals"
        elif input_param=="masale" or input_param=="spice" or input_param=="masala" or input_param=="spices":
            return "spices"
        elif input_param=="floor" or "ata" or "aataa" or "aata" or "flour":
            return "floor"


def products_list(request, p_n):
    total_pages = int(int(product.objects.all().count())/9)+1
    temp_l = []
    filter_response=None
    # curre = pagination_function(p_n, product.objects.all(), product.objects.all().count())
    # filter_flag=0

    all_products_list = product.objects.all()
    current_all_list = product.objects.all()
    current_page_list = pagination_function(int(p_n), all_products_list, len(all_products_list))

            # p_l=temp_l
    # if filter_flag==0:
        # p_l = pagination_method(p_n, product.objects.all(), product.objects.all().count())
    # else:
        # p_l=pagination_method(p_n, temp_l, len(temp_l))
    # no_of_prod = p_l.count()
    # no_of_pages=int(no_of_prod/9))+1
    if request.is_ajax():
        if request.method=="POST":
            if 'request_type' in request.POST:
                the_product_id = int(request.POST['product_id'])
                amount = int(request.POST['amount'])
                the_product = product.objects.get(pk=the_product_id)
                to_pay = int((the_product.price/the_product.base_quantity)*amount)
                h = shopping_cart_items(user=request.user, product_id=the_product, quantity=amount, amount_to_pay=to_pay)
                h.save()
            # elif 'product_filters' in request.POST:
            # #seperating the words or the values from the JSON data string
            #
            #     filter_list = str(request.POST['product_filters'])
            #     filter_list = filter_list.split('&')
            #         # print(filter_list)
            #     # current_all_list = product.objects.all()
            #     if(len(filter_list)>1):
            #         filter_flag=1
            #         #converting the json data into list of strings
            #         final_list=[]
            #         for i in range(len(filter_list)):
            #             final_list.append(filter_list[i].split('='))
            #             final_list[i-1] = final_list[i-1].pop()
            #         ss = final_list[len(final_list)-1]
            #         final_list[len(final_list)-1]=final_list[len(final_list)-1][:len(ss)-1]
            #         # p_l = p_l.filter(product_type=final_list[0])
            #         filter_response=final_list
            #         print("filter response = "+str(filter_response))
            #         print(final_list)
            #         # print("P_L = "+str(p_l))
            #         for term in final_list:
            #             for f in range(len(p_l)):
            #                 if current_all_list[f].product_type==term:
            #                     temp_l.append(p_l[f])
            #         current_page_list=pagination_method(1, temp_l, len(temp_l))
            #         total_pages = int(int(len(current_page_list))/9)+1
        # elif request.method=="GET":
        #     if 'get_page_' in request.GET:
        #         page_no = int(request.GET['get_page_'])
        #         print("current_all_list = "+str(current_all_list))
        #         current_page_list = pagination_function(page_no, current_all_list, len(current_all_list))
        #         print("current_page_list = "+str(current_page_list))
        #         print("current_page_list = "+str(current_page_list))
        #         current_page_products_id = []
        #         for items in current_page_list:
        #             current_page_product_id.append(item.id)
        #         return HttpResponse(current_page_product_id)
                # return render(request, 'products.html', {'products_list': current_page_list, 'previously_requested':filter_response, 'no_of_pages':total_pages, 'current_page':p_n})


    # filter_response=None

    # print()
    if request.method == "GET":
        if 'search_keyword' in request.GET:
            # print("GET METHOD")
            search_keyword =  request.GET.get('search_keyword')
            # all_product_names = []
            all_product_types = ["spices", "cereals", "flours", "flour" , "masale", "spice", "dal", "daal", "daals", "cereal", "pulses", "aata", "pulse", "masala", "spice"]
            products_query_set = current_all_list

            p_s_o = product_search_object() #reference above specified product_search_object class
            for i in current_all_list:
                p_s_o.add_to_list(i)
            current_all_list=[]
            # filter_response=None
            res = p_s_o.find_word(search_keyword)
            # print(res)
            if res: #searching products using product name
                if type(res) == list:
                    for i in range(len(res)):
                        # print("res[i] = "+str(res[i]))
                        current_all_list.append(product.objects.filter(product_name=res[i])[0])
                else:
                    current_all_list.append(product.objects.get(product_name=res))
            elif search_keyword in all_product_types: #searching products using catogory
                search_keyword=search_parameter(search_keyword)
                current_all_list = current_all_list.objects.filter(product_type=search_keyword)
            current_page_list=pagination_function(int(p_n), current_all_list, len(current_all_list))
            # print("current_all_list = "+str(current_all_list))
            total_pages = int(int(len(current_page_list))/9)+1
        # return render(request, 'products.html', {'products_list': p_l, 'previously_requested':filter_response})
    # print(p_l)
    return render(request, 'products.html', {'products_list': current_page_list, 'previously_requested':filter_response, 'no_of_pages':total_pages, 'current_page':p_n})

def pagination_function(page_no, all_objects, no_of_prod):
    # no_of_prod = int(all_objects.count())
    page_no=int(page_no)
    # print("no_of_prod = "+str(no_of_prod))
    # print("page_no = "+(str(page_no)))
    # all_objects = product.objects.all()
    # print("all_objects = "+str(all_objects))
    limited_objects = []
    this_page_count = 0

    lower_limit=(page_no-1)*9 #perfect
    # l1 = int(page_no*9)
    if page_no*9>=no_of_prod:
        this_page_count = no_of_prod
    elif page_no*9<no_of_prod:
        this_page_count = 9*page_no
    # print("this_page_count = "+str(this_page_count))
    # print("lower_limit = "+str(lower_limit))
    for i in range(lower_limit, this_page_count):
        limited_objects.append(all_objects[i])

    return limited_objects
