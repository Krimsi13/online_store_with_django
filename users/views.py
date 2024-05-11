import random
import secrets
import string


from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView

from users.forms import UserRegisterForm
from users.models import User

from config.settings import EMAIL_HOST_USER


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject="Подтверждение почты",
            message=f"Подтвердите вашу почту по ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


# class ResetPassword(TemplateView):
#     def post(self, request):
#         mail = request.POST.get('mail')
#         user = get_object_or_404(User, email=mail)
#
#         letters = list(string.ascii_lowercase)
#         new_password = ''
#         for _ in range(5):
#             new_password = new_password + random.choice(letters) + str(random.randint(1, 9))
#
#         user.set_password(new_password)
#         user.save()
#
#         send_mail(
#             subject="Новый пароль",
#             message=f"Ваш новый пароль: {new_password}",
#             from_email=EMAIL_HOST_USER,
#             recipient_list=[user.email],
#         )
#
#         return redirect("users:login")


def reset_password(request):
    if request.method == 'GET':
        return render(request, 'users/reset_password.html')

    if request.method == 'POST':
        mail = request.POST.get('mail')
        user = get_object_or_404(User, email=mail)

        letters = list(string.ascii_lowercase)
        new_password = ''
        for _ in range(5):
            new_password = new_password + random.choice(letters) + str(random.randint(1, 9))

        user.set_password(new_password)
        user.save()

        send_mail(
            subject="Новый пароль",
            message=f"Ваш новый пароль: {new_password}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return redirect(reverse("users:login"))
