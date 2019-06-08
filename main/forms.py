from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Account


class AccountCreationForm(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter username',
                'id': 'registerUsernameInput'
            },
        ),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter email',
                'id': 'registerEmailInput'
            },
        ),
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Password',
                'id': 'registerPassword1Input'
            },
        ),
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password',
                'id': 'registerPassword2Input'
            },
        ),
    )
    date_born = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Account
        fields = ['username', 'email', 'password1', 'password2', 'date_born']

    def save(self, commit=True):
        user = super(AccountCreationForm, self).save(commit=False)
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.password = self.cleaned_data.get('password1')
        user.date_born = self.cleaned_data.get('date_born')

        if commit:
            user.save()
        return user

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email


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
