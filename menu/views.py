from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Dish
import random

def today_menu(request):
    today = timezone.now().date()
    dishes = list(Dish.objects.all())

    recommendations = []
    if dishes:
        dishes.sort(key=lambda d: d.last_cooked_date or timezone.datetime.min.date())
        candidate_pool = dishes[:6]
        sample_count = min(3, len(candidate_pool))
        recommendations = random.sample(candidate_pool, sample_count)

    return render(request, 'menu/today_menu.html', {
        'today': today,
        'recommendations': recommendations
    })

def cook_dish(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    dish.last_cooked_date = timezone.now().date()
    dish.save()
    return redirect('today_menu')

# ログイン不要で誰でも料理を登録できる画面
def add_dish(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        memo = request.POST.get('memo', '')
        if name:
            Dish.objects.create(name=name, memo=memo)
            return redirect('today_menu')

    return render(request, 'menu/add_dish.html')