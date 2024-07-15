from django.urls import path
from users.apps import UsersConfig
# from django.contrib.auth.views import LoginView, LogoutView

from users.views import CreateUserView, CustomLoginView

app_name = UsersConfig.name

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    # path('logout/', logout, name='logout'),
    path('register/', CreateUserView.as_view(), name='register'),
]
