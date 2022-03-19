from .models import *
from django.urls import reverse_lazy


class BaseMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        if not self.request.user.is_authenticated:
            context['is_auth'] = False
            context['login'] = {'title': 'Log In', 'name': 'login'}
            context['signin'] = {'title': 'Sign In', 'name': 'signin'}
        else:
            context['is_auth'] = True
            context['profile'] = {'title': 'Профиль', 'name': 'profile'}
        return context

    def is_auth(self):
        if not self.request.user.is_authenticated:
            return reverse_lazy('login')
