from django import forms
from django.forms import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Account, Profile


def validate_username(username):
    if ' ' in username:
        raise ValidationError(
            _('%(username)s Cant contain space'),
            params={
                'username': username
            }
        )
    if '@' in username:
        raise ValidationError(
            _('%(username)s can\' contain "@"'),
            params={
                'username': username
            }
        )


def validate_email(email):
    if Account.objects.filter(email=email).exists():
        raise ValidationError('Email already exists')


def validate_date_born(date_born):
    if timezone.now().date() - date_born < timezone.timedelta(6574):
        raise ValidationError(
            _('%(date_born)s should be more than 18'),
            params={
                'date_born': date_born
            }
        )


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
        validators=[validate_username]
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
        validators=[validate_email]
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
        widget=forms.SelectDateWidget(
            years=[x for x in range(1940, timezone.now().date().year + 1)],
            attrs={
                'class': 'form-control',
            },
        ),
        validators=[validate_date_born]
    )

    class Meta:
        model = Account
        fields = ['username', 'email', 'password1', 'password2', 'date_born']

    def save(self, commit=True):
        user = super(AccountCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        user.date_born = self.cleaned_data['date_born']

        if commit:
            user.save()
        return user

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise ValidationError("You must confirm your password")
        if password1 != password2:
            raise ValidationError("Your passwords do not match")
        return password2


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

class ProfileCreationForm(forms.ModelForm):

    image = forms.ImageField(
        label="Profile Picture",
        widget=forms.FileInput(),
    )

    class Meta:
        model = Profile
        fields = ['image'] 
