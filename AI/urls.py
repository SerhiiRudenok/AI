from myapp.views import index_page
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page, name='index'),
    #path('register/', register_page, name='register'),
]