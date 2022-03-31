from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
import functions as f

from .models import *


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class MasterPassForm(forms.Form):
    masterpass = forms.CharField(label='Master-пароль', widget=forms.TextInput(attrs={'class': 'form-input'}))

    def clean_masterpass(self):

        login = self.data['username']

        secret = self.cleaned_data["masterpass"]

        id = User.objects.get(username=login).id

        privatekey = UserKeys.objects.get(user_id=id).private_key

        res = f.symmetrical_dec(privatekey, secret)

        if not res:
            raise ValidationError("Master-пароль не подходит")
        
        return secret
    

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class FolderCreateForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Folder
        fields = ['name',]

    def save(self, request):
        fol = Folder.objects.create(name=self.data['name'])
        fol.save()
        UserFolder.objects.create(user_id=request.user.id, folder_id=fol.id)
        UserAdmin.objects.create(folder_id=fol.id, user_id=request.user.id)


class AccessCreateForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-input'}))
    value = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Access
        fields = ['name', 'value']

    def save(self, request, pk):
        ac = Access.objects.create(name=self.data['name'], value=self.data['value'], folder_id=pk)
        ac.save()
        UserAccess.objects.create(user_id=request.user.id, access_id=ac.id)