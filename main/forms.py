from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account


class AccountCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model=Account
        fields=('username', 'email', 'password1', 'password2')

    def save(self, commit = True):
        user=super(AccountForm, self).save(commit = False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user
