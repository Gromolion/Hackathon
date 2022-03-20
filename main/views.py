from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.db.utils import IntegrityError

from .forms import *
from .utils import *


class Home(BaseMixin, ListView):
    model = File
    template_name = 'main/home.html'
    context_object_name = 'objects'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['projects'] = Project.objects.filter(panel__userpanel__user=self.request.user.id)
        con_def = self.get_user_context(title='Главная страница')
        return context | con_def

    # def get_queryset(self):
    #     return Project.objects.all()

    # def get_panels(self, project_id):
    #     return Panel.objects.filter(project_id=project_id, panel__userpanel__user_id=self.request.user.id)
    #
    # def get_infos(self, panel_id):
    #     return Info.objects.filter(panel_id=panel_id)
    #
    # def get_superusers(self, panel_id):
    #     return User.objects.filter(userpanel__panel_id=panel_id, userpanel__is_admin=True)
    #
    # def get_users(self, panel_id):
    #     return User.objects.filter(userpanel__panel_id=panel_id, userpanel__is_admin=False)


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
