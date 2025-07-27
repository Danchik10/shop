from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django import forms
from users.models import User

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Введите имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Введите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'password')

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Введите имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Введите фамилию'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Введите имя'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs = {'placeholder' : 'Введите почту'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    image = forms.ImageField(widget=forms.FileInput(), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly' : True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'readonly' : True}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')