from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from users.forms import UserRegistrationForm, UserProfileForm, UserLoginForm

from products.models import Basket
from .serializer import UserLoginSerializer, UserRegistrationSerializer, UserProfileSerializer, UserBasketSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from .models import User

def registration(request):
        # 1. Если запрос POST - обрабатываем форму
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)           #Создать форму с данными
        if form.is_valid():
            user = form.save()          #Сохранить пользователя
            login(request, user)            #Если данные валидны, сохраняем пользователя и выполняем вход с помощью функции login        
            return redirect("users:login")  #Перенаправить на страницу входа после регистрации 
            
    # 2. Если GET - показать пустую форму
    else:
        form = UserRegistrationForm()       #Создать пустую форму
    context = { 'form' : form }
    return render(request, "users/registration.html", context)

def user_login(request):
    form = UserLoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            #Получение данных из формы
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)     #Проверяет, есть ли пользователь с таким логином/паролем в базе.
        if user is not None:
            login(request, user)         #Создает сессию пользователя (авторизует).
            return redirect("index")
    context = { 'form' : form }
    return render(request, "users/user_login.html", context)
#--------------------------------API-------------------------------#
class UserAuthAPIView(viewsets.ViewSet):  #не прописываю queryset, .... Значит ссылка api/entrance/ не будет работать
    @action(detail=False, methods=['post'], permission_classes=(AllowAny,))
    def registration(self, request):
        serializer = UserRegistrationSerializer(data=request.data)  #создаю экземпляр сериализатора с данными из запроса
        serializer.is_valid(raise_exception=True)       #Сериализатор преобразует эти данные в объект Python и начинает валидацию
        user = serializer.save()  #сохранение в бд
        token, created = Token.objects.get_or_create(user=user)     #Создаёт токен для нового пользователя
        return Response({'user' : UserProfileSerializer(user).data,
                         'token' : token.key})          
    @action(detail=False, methods=['post'], permission_classes=(AllowAny,))
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, create = Token.objects.get_or_create(user=user)
        return Response({'user' : UserProfileSerializer(user).data,
                         'token' : token.key})
#--------------------------------API-------------------------------#

@login_required     #встроенный декоратор - проверяет, авторизован ли пользователь. Если пользователь не вошёл в систему, он будет автоматически перенаправлен на страницу входа.
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)  #последняя переменная нужна для загрузки фото профиля
        if form.is_valid():
            form.save()
            return redirect("users:profile")
    else:
        form = UserProfileForm(instance=request.user)       #при GET-запросе форма заполняется данными из существующего профиля
    
    baskets = Basket.objects.filter(user=request.user)
    total_sum = sum(basket.sum() for basket in baskets)
    total_quantity = sum(basket.quantity for basket in baskets)

    context = {
        'form' : form,
        'baskets' : Basket.objects.filter(user=request.user),
        'total_sum' : total_sum,
        'total_quantity' : total_quantity,
        }
    return render(request, 'users/profile.html', context)
#--------------------------------API-------------------------------#
class UserProfileAPIView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    @action(methods=['put', 'get'], detail=False)
    def profile(self, request):
        user = request.user #Текущий пользователь
        if request.method == 'GET':
            serializer = UserProfileSerializer(user)
            return Response(serializer.data) 
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(request.user, data=request.data, partial=True)  #partial=True разрешает частичное обновление
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data) 
    
    @action(methods=['get'], detail=False)
    def user_basket(self, request):
        baskets = Basket.objects.filter(user=request.user)
        total_sum = sum(basket.sum() for basket in baskets)
        total_quantity = sum(basket.quantity for basket in baskets) 
        serializer = UserBasketSerializer({
            'total_sum' : total_sum,
            'total_quantity' : total_quantity,
            'items' : [{
                'id' : basket.id,
                'product' : basket.product.name,
                'quantity' : basket.quantity,
                'price' : basket.product.price
            } for basket in baskets]
        })
        return Response(serializer.data)
#--------------------------------API--------------------------------#



@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))       