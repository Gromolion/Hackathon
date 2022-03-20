from .models import *
from django.urls import reverse_lazy
from django.shortcuts import redirect


class BaseMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        if not self.request.user.is_authenticated:
            context['is_auth'] = False
            return context
        else:
            context['is_auth'] = True
            return context

    def is_auth(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
