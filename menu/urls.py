from django.urls import path
from . import views

urlpatterns = [
    path('', views.today_menu, name='today_menu'),
    path('cook/<int:pk>/', views.cook_dish, name='cook_dish'),
]