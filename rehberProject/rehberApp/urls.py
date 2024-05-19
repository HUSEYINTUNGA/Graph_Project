from django.urls import path
from . import views

urlpatterns = [
    path('',views.Anasayfa),
    path('AboutWe' , views.AboutWe),
    path('location/<str:location_name>/', views.location, name='location'),
]
