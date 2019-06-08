from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Account


class AccountCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(AccountCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class AccountAuthentication(forms.Form):

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'aria-describedby': 'emailHelp',
                'placeholder': 'Enter email',
                'id': 'loginEmailInput',
            },
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'id': 'loginPasswordInput',
            },
        ),
    )

    class Meta:
        model = User
        # widgets = {
        #     'email': forms.EmailInput(attrs={'class': 'form-control', 'aria-describedby': 'emailHelp', 'placeholder': 'Enter email'}),
        #     'password' : forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Password' })
        #     class="form-control" id="exampleInputPassword1" placeholder="Password">
        # }

    def authenticate_via_email(self):
        email = self.cleaned_data['email']
        if email:
            try:
                user = User.objects.get(email__iexact=email)
                if user.check_password(self.cleaned_data['password']):
                    return user
            except ObjectDoesNotExist:
                pass
        return None
