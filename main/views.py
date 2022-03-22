from doctest import master
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.utils import IntegrityError
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, ListView

import functions as f

from .forms import *
from .utils import *


class Home(LoginRequiredMixin, BaseMixin, ListView):
    model = Folder
    template_name = 'main/home.html'
    context_object_name = 'objects'
    login_url = 'login'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['folders'] = Folder.objects.filter(access__useraccess__user_id=self.request.user.id).distinct()
        context['user_id'] = self.request.user.id
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


def home(request):
    data = {
        'title': 'Менеджер паролей',
    }
    form = FolderCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        UserAdmin.objects.create()

def register(request):
    data = {
        'title': 'Регистрация',
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

        login = registerform.cleaned_data.get('username')     

        public, encrypted_private = f.symmetrical_enc(masterpass)

        id = User.objects.get(username=login).id

        masterform.get_login(id)

        user = {
            "user_id": id,
            "public_key": public,
            "private_key": repr(encrypted_private)
        }

        UserKeys.objects.create(**user)

        return redirect('login')
    return render(request, 'main/signin.html', data | {'registerform': registerform, 'masterform': masterform})


class LoginUser(BaseMixin, LoginView):
    form_class = LoginUserForm

    template_name = 'main/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        masterform = MasterPassForm()
        context = super().get_context_data(**kwargs)
        
        context["form2"] = masterform
        con_def = self.get_user_context(title='Войти')
        return context | con_def

    def get_success_url(self):
        return reverse_lazy('home')


def login(request):
    data = {
        'title': 'Войти',
    }

    loginform = LoginUserForm(request.POST)
    masterform = MasterPassForm(request.POST)
    if request.method == 'POST' and loginform.is_valid() and masterform.is_valid():
        

        return redirect('home')

    data["form"] = loginform
    data["form2"] = masterform

    return render(
        request, 
        template_name='main/login.html',
        context=data
    )

    # return render(request, 'main/signin.html', data | {'registerform': registerform, 'masterform': masterform})



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


def foldercreate(request):
    form = FolderCreateForm

    return render(request, 'main/foldercreate.html')