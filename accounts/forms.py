from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UsernameField
)
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'autofocus': False,
                'class': 'form-control',
                'placeholder': 'username',
            }
        )
    )
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'class': 'form-control',
                'placeholder': 'password',
            }
        ),
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self._update_errors_list()

    def _update_errors_list(self):
        self.error_messages.update(
            {
                'unconfirmed_email': (
                    'Ваша учётная запись не активирована. Для активации вашей '
                    'учётной записи перейдите по ссылке из письма, которое '
                    'было выслано на email, который вы указали при регистрации.'
                ),
            }
        )

    def confirm_login_allowed(self, user):
        if not user.is_active and not user.last_login:
            raise ValidationError(
                self.error_messages['unconfirmed_email'],
                code='unconfirmed_email',
            )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя',
        min_length=5,
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'username',
            },
        ),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'name@example.com',
            },
        ),
    )
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'password',
            },
        ),
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'password',
            },
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._update_errors_list()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
        except ObjectDoesNotExist:
            return self.cleaned_data['email']
        else:
            raise ValidationError(
                self.error_messages['registered_email'],
                code='registered_email'
            )

    def _update_errors_list(self):
        self.error_messages.update(
            {
                'registered_email': (
                    'Пользователь с таким email адресом уже существует.'
                ),
            }
        )
