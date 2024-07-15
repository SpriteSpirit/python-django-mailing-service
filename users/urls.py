from django.urls import path
from users.apps import UsersConfig

from users.views import CreateUserView, CustomLoginView, CustomLogoutView
# from django.contrib.auth.views import LogoutView

app_name = UsersConfig.name

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'), # можно ли обойтись без шаблона?
    path('register/', CreateUserView.as_view(), name='register'),
]
