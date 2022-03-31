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
    form_class1 = FolderCreateForm
    form_class2 = AccessCreateForm
    success_url = 'home'
    template_name = 'main/home.html'
    login_url = 'login'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        context['folders'] = Folder.objects.filter(userfolder__user_id=user_id)
        context['user_id'] = user_id
        context['form1'] = self.form_class1()
        context['form2'] = self.form_class2()
        try:
            pk = self.kwargs['pk']
        except KeyError:
            pk = None
        context['selected'] = pk
        if pk:
            context['accesses'] = Access.objects.filter(folder_id=pk, useraccess__user_id=user_id)
            context['users'] = User.objects.filter(useraccess__access__folder_id=pk).distinct()
            context['admins'] = User.objects.filter(useradmin__folder_id=pk)
            context['is_admin'] = User.objects.filter(useradmin__folder_id=pk, useradmin__user_id=user_id)
        con_def = self.get_user_context(title=Folder.objects.get(id=pk) if pk else 'Главная страница')
        return context | con_def

    def post(self, request, pk):
        form1 = self.form_class1(request.POST)
        form2 = self.form_class2(request.POST)
        if request.method == 'POST':
            if 'folder-but' in request.POST and form1.is_valid():
                form1.save(request)
                return redirect('home')
            elif 'access-but' in request.POST and form2.is_valid():
                form2.save(request, self.kwargs['pk'])
                return redirect(request.META.get('HTTP_REFERER'))


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
        context['folders'] = Folder.objects.filter(useradmin__user_id=self.request.user.id)
        context['users'] = User.objects.filter(useraccess__access__folder_id=self.kwargs['pk']).distinct()
        context['admins'] = User.objects.filter(useradmin__folder_id=self.kwargs['pk'])
        context['user_id'] = self.request.user.id
        context['selected'] = Folder.objects.get(id=self.kwargs['pk']).id
        con_def = self.get_user_context(title=Folder.objects.get(id=self.kwargs['pk']))
        return context | con_def

    def get_queryset(self):
        return Access.objects.filter(folder_id=self.kwargs['pk'], useraccess__user_id=self.request.user.id)
