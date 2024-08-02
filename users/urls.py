from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from django.urls import path, reverse_lazy
from django.views.decorators.cache import cache_page

from users.apps import UsersConfig

from users.views import CustomLoginView, CustomLogoutView, UserCreateView, UserDetailView, UserUpdateView, \
    UserListView, UserCheckBlockView, email_verification, CustomPasswordResetView

app_name = UsersConfig.name

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # можно ли обойтись без шаблона?
    path('register/', UserCreateView.as_view(), name='register'),
    path('profile/<int:pk>', UserDetailView.as_view(), name='profile'),
    path('update/<int:pk>', UserUpdateView.as_view(), name='update'),
    path('user_list/', cache_page(60)(UserListView.as_view()), name='user_list'),
    path('block_page/', UserCheckBlockView.as_view(), name='block_page'),

    path('email_confirm/<str:token>/', email_verification, name='email_confirm'),

    path('password_reset/',
         CustomPasswordResetView.as_view(template_name='users/password_reset.html',
                                         success_url=reverse_lazy('users:password_reset_done'),
                                         html_email_template_name='users/password_reset_email.html'),
         name='password_reset'),

    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<str:token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                          success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),

    path('password_reset_complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
