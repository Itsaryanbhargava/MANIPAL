from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('add_category/',views.add_category,name='add_category'),
    path('add_page/',views.add_page,name='add_page'),
]