from django.urls import path

from users.views import user_login, registration, profile, logout_view

app_name = "users"

urlpatterns = [
    path('login/', user_login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout')
]