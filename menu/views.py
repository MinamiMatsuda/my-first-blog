from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Dish
import random

def today_menu(request):
    today = timezone.now().date()
    dishes = list(Dish.objects.all())

    recommendations = []
    if dishes:
        # 最後に作った日が古いもの（または未設定）順に並べ替え
        dishes.sort(key=lambda d: d.last_cooked_date or timezone.datetime.min.date())
        # ごぶさたな上位候補（最大6品）の中から重ならないようにランダムで最大3品選出
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