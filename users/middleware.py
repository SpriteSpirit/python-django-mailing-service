from django.shortcuts import redirect
from django.urls import reverse


class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Пропускаем проверку для URL-адреса выхода
        if request.path == reverse('users:logout'):  # Замените 'users:logout' на фактическое имя вашего URL-адреса выхода
            return self.get_response(request)

        if request.user.is_authenticated and request.user.is_blocked:
            if request.path != reverse('users:block_page'):
                return redirect(reverse('users:block_page'))
        return self.get_response(request)
