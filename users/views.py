from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from users.forms import UserRegistrationForm, UserProfileForm, UserLoginForm

from products.models import Basket

def registration(request):
        # 1. Если запрос POST - обрабатываем форму
    if request.method == 'POST':
        #Создать форму с данными
        form = UserRegistrationForm(request.POST)
        #Проверить валидность
        if form.is_valid():
        #Сохранить пользователя
            user = form.save()
            login(request, user)
        #Перенаправить куда-то
            return redirect("users:login")
            
    # 2. Если GET - показать пустую форму
    else:
        #Создать пустую форму
        form = UserRegistrationForm()
    context = { 'form' : form }
    return render(request, "users/registration.html", context)

def user_login(request):
    form = UserLoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            #Получение данных из формы
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #Проверяет, есть ли пользователь с таким логином/паролем в базе.
            user = authenticate(username=username, password=password)
        if user is not None:
            #Создает сессию пользователя (авторизует).
            login(request, user)
            return redirect("index")
    context = { 'form' : form }
    return render(request, "users/user_login.html", context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("users:profile")
    else:
        form = UserProfileForm(instance=request.user)
    
    baskets = Basket.objects.filter(user=request.user)
    total_sum = sum(basket.sum() for basket in baskets)
    total_quantity = sum(basket.quantity for basket in baskets)

    context = {
        'form' : form,
        'basket' : Basket.objects.filter(user=request.user),
        'total_sum' : total_sum,
        'total_quantity' : total_quantity,
        }
    return render(request, 'users/profile.html', context)  

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))       