from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.db.utils import IntegrityError

from .forms import *
from .utils import *


class Home(BaseMixin, ListView):
    model = Project.objects.select_related('Panel', 'auth.User', 'Info', 'UserPanel')
    template_name = 'main/home.html'
    context_object_name = 'objects'

    # extra_context = {'title': 'Главная страница'} передача статических элементов в контекст

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        con_def = self.get_user_context(title='Главная страница')
        return context | con_def

    def get_queryset(self):
        return User.objects.raw(
            '''SELECT main_project.id, main_project.title AS project_title, auth_user.username as username, 
            main_panel.title as panel, main_info.name as info, main_info.value as value
             FROM main_project
             INNER JOIN main_panel ON main_project.id = main_panel.project_id
             INNER JOIN main_userpanel ON main_userpanel.panel_id = main_panel.id
             INNER JOIN auth_user ON auth_user.id = main_userpanel.user_id
             INNER JOIN main_info ON main_info.panel_id = main_panel.id
             WHERE auth_user.id=%(user.id)s''' % {'user.id': self.request.user.id})


def register(request):
    data = {
        'title': 'Регистрация',
        'profile': {'title': 'Профиль'},
        'login': {'title': 'Log In'},
        'signin': {'title': 'Sign In'}
    }
    registerform = RegisterUserForm(request.POST or None)
    masterform = MasterPassForm(request.POST or None)
    if request.method == 'POST' and registerform.is_valid():
        try:
            registerform.save()
        except IntegrityError:
            registerform.add_error('username', 'Такой логин уже существует')
        masterform.is_valid()
        masterpass = masterform.cleaned_data['masterpass']
        print(masterpass)
        # user = UserKeys.objects.get(user_id=request.user.id)
        # user['publickey'] = b'publickey'
        # user['secretkey_enc'] = b'secretkey'
        # user.save()
        return redirect('.')
    return render(request, 'main/signin.html', data | {'registerform': registerform, 'masterform': masterform})


class LoginUser(BaseMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        con_def = self.get_user_context(title='Войти')
        return context | con_def

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')
