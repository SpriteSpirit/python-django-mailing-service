from django.urls import path
from users.apps import UsersConfig

from users.views import CustomLoginView, CustomLogoutView, UserCreateView, UserDetailView, UserUpdateView, UserListView, \
    UserCheckBlockView

# from django.contrib.auth.views import LogoutView

app_name = UsersConfig.name

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # можно ли обойтись без шаблона?
    path('register/', UserCreateView.as_view(), name='register'),
    path('profile/<int:pk>', UserDetailView.as_view(), name='profile'),
    path('update/<int:pk>', UserUpdateView.as_view(), name='update'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('block_page/', UserCheckBlockView.as_view(), name='block_page'),
]
