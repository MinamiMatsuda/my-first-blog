from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.utils import timezone
from .models import Dish
import random

# あなたとお母さんだけの秘密の合言葉
SECRET_KEY_VALUE = 'chiyo2026'

def verify_key(request):
    # URLの ?key= またはクッキー（記憶）で合言葉が合っているかチェック
    return request.GET.get('key') == SECRET_KEY_VALUE or request.session.get('authorized') == True

def today_menu(request):
    # 合言葉のチェック（初回はURL、2回目以降はセッションで記憶）
    if request.GET.get('key') == SECRET_KEY_VALUE:
        request.session['authorized'] = True

    if not request.session.get('authorized'):
        raise Http404("ページが見つかりません")

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
    if not request.session.get('authorized'):
        raise Http404("ページが見つかりません")

    dish = get_object_or_404(Dish, pk=pk)
    dish.last_cooked_date = timezone.now().date()
    dish.save()
    return redirect('today_menu')

def add_dish(request):
    if not request.session.get('authorized'):
        raise Http404("ページが見つかりません")

    if request.method == 'POST':
        name = request.POST.get('name')
        memo = request.POST.get('memo', '')
        if name:
            Dish.objects.create(name=name, memo=memo)
            return redirect('today_menu')

    return render(request, 'menu/add_dish.html')

def dish_list(request):
    if not request.session.get('authorized'):
        raise Http404("ページが見つかりません")

    dishes = Dish.objects.all().order_by('name')
    return render(request, 'menu/dish_list.html', {'dishes': dishes})