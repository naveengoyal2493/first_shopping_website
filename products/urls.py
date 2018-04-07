from django.conf.urls import url
from . import views, delievery_orders, product_views, product_search, product_views_1
app_name='products'

urlpatterns = [
url(r'^$', views.home, name='home'),
url(r'^register/$', views.UserFormView.as_view(), name='register_user'),
url(r'^login_user/$', views.login_user, name='login_user'),
url(r'^profile/(?P<account_id>[0-9]+)/$', views.user_profile, name='user_info'),
url(r'^logout_user/$', views.logout_user, name='logout_user'),
url(r'^enter_address/$', views.add_address, name='add_user_address'),
url(r'^all_orders/$', views.view_all_user_orders, name='view_user_orders'),
url(r'^products/(?P<p_n>[0-9]+)/$', product_views.products_list, name='products_list'),
url(r'^check_orders/$', delievery_orders.view_orders, name='view_orders'),
url(r'^products/search/$', product_search.search, name='search_products'),
url(r'^shopping_cart/$', views.shopping_cart, name='cart'),
url(r'^about_us/$', views.aboutus, name='about_us_page')
]
