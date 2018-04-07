from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('products.urls'))
]

urlpatterns+=static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
admin.site.site_header = 'ShriBariStores Admin Panel'
