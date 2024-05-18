from django.urls import path
from . import views

urlpatterns = [
    path('',views.Anasayfa),
    path('aboutWe' , views.AboutWe),
]
