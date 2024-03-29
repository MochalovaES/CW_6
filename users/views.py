from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from users.forms import RegisterForm, ModeratorForm, UserForm
from users.models import User
from django.utils.crypto import get_random_string


class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        self.object = form.save()
        self.object.is_active = False
        self.object.verify_code = get_random_string(12)
        self.object.save()
        url = f'http://127.0.0.1:8000/users/email/verify/{self.object.verify_code}'
        send_mail(
                subject='Регистрация',
                message=f'Для успешной регистрации перейдите по ссылке: {url}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.object.email],
                fail_silently=False,
            )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:verify_message')


def verification(request, verify_code):
    try:
        user = User.objects.filter(verify_code=verify_code).first()
        user.is_active = True
        user.save()
        return redirect('users:success_verify')
    except (AttributeError, ValidationError):
        return redirect('users:invalid_verify')


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('users:list_view')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users:users_list')


@login_required
@permission_required(['users.view_user', 'users.set_is_active'])
def get_users_list(request):
    users_list = User.objects.all()
    context = {
        'object_list': users_list,
        'title': 'Список пользователей сервиса',
    }
    return render(request, 'users/users_list.html', context)

