from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.db.utils import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .utils import *


class Home(LoginRequiredMixin, BaseMixin, ListView):
    model = Folder
    template_name = 'main/home.html'
    context_object_name = 'objects'
    login_url = 'login'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['folders'] = Folder.objects.filter(access__useraccess__user_id=self.request.user.id).distinct()
        context['user_id'] = self.request.user.id
        context['get_users'] = self.get_users
        con_def = self.get_user_context(title='Главная страница')
        return context | con_def

    def get_queryset(self):
        return Folder.objects.all()

    # def get_accesses(self, folder_id):
    #     return Access.objects.filter(folder_id=1, useraccess__user_id=self.request.user.id)

    def get_admins(self, folder_id):
        return User.objects.filter(useradmin__folder_id=folder_id)

    def get_users(self, access_id):
        return User.objects.filter(useraccess__access_id=access_id)


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
        return redirect('login')
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


class FolderView(LoginRequiredMixin, BaseMixin, ListView):
    model = Access
    template_name = 'main/folder.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'accesses'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['folders'] = Folder.objects.filter(access__useraccess__user_id=self.request.user.id).distinct()
        context['users'] = User.objects.filter(useraccess__access__folder_id=self.kwargs['pk']).distinct()
        context['admins'] = User.objects.filter(useradmin__folder_id=self.kwargs['pk'])
        context['user_id'] = self.request.user.id
        con_def = self.get_user_context(title=Folder.objects.get(id=self.kwargs['pk']))
        return context | con_def

    def get_queryset(self):
        return Access.objects.filter(folder_id=self.kwargs['pk'], useraccess__user_id=self.request.user.id)

