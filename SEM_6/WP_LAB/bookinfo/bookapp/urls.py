from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('metadata/',views.metadata,name='metadata'),
    path('reviews/',views.reviews,name='reviews'),
    path('publisher/',views.publisher,name='publisher'),
]