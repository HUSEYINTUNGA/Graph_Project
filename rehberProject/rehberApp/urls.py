from django.urls import path
from . import views

urlpatterns = [
    path('',views.Anasayfa),
    path('<str:country>' , views.getProductByCountry)
]
