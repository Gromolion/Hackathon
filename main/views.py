from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import RegisterUserForm
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


class RegisterUser(BaseMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/signin.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        con_def = self.get_user_context(title='Sign In')
        return context | con_def


def login(request):
    pass


def profile(request):
    pass
