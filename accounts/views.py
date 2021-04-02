from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    logout_then_login,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordResetDoneView,
    PasswordResetView
)
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView

from accounts.forms import DeactivationForm, LoginForm, SignUpForm
from accounts.services import activate_email
from accounts.tasks import (
    deactivate_user as _deactivate_user,
    send_activation_email
)


class LogoutRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class ActivateUserView(TemplateView):
    template_name = 'accounts/activate_user.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_active:
            message = 'Ваша учётная запись была активирована ранее.'
        else:
            message = activate_email(kwargs['link'])
        return self.render_to_response({'message': message})


class DeactivateUserView(LoginRequiredMixin, FormView):
    template_name = 'accounts/deactivate_user.html'
    form_class = DeactivationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, request, *args, **kwargs):
        return self.render_to_response({'form': self.form_class})

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            transaction.on_commit(
                lambda: _deactivate_user.delay(
                    form.cleaned_data['username']
                )
            )
            return logout_then_login(request)
        return super().post(request, *args, **kwargs)


class _LoginView(LoginView):
    authentication_form = LoginForm
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = form.get_user()
            if not user.is_active:
                site = str(get_current_site(request))
                transaction.on_commit(
                    lambda: send_activation_email.delay(
                        user.pk,
                        user.email,
                        site,
                        True
                    )
                )
                return redirect('reactivate_user', user=user.username)
        return super().post(request, *args, **kwargs)


class _LogoutView(LogoutView):
    next_page = '/'
    template_name = 'accounts/logged_out.html'


class _PasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change_form.html'


class _PasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


class _PasswordResetView(LogoutRequiredMixin, PasswordResetView):
    template_name = 'accounts/password_reset_form.html'


class _PasswordResetCompleteView(LogoutRequiredMixin, PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class _PasswordResetConfirmView(LogoutRequiredMixin, PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'


class _PasswordResetDoneView(LogoutRequiredMixin, PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class ReactivateUserView(LogoutRequiredMixin, TemplateView):
    template_name = 'accounts/reactivate_user.html'

    def get(self, request, *args, **kwargs):
        message = (
            'На ваш email, указанный при регистрации на нашем сайте, была '
            'выслана ссылка для повторной активации аккаунта.'
        )
        return self.render_to_response({'message': message})


class SignUpView(LogoutRequiredMixin, CreateView):
    form_class = SignUpForm
    template_name = 'accounts/sign_up.html'

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            site = str(get_current_site(request))
            transaction.on_commit(
                lambda: send_activation_email.delay(
                    user.pk,
                    form.cleaned_data['email'],
                    site,
                    False
                )
            )
            messages.success(
                request,
                'Письмо с ссылкой для активации было отправлено на ваш email.'
            )
            return redirect('home')
        else:
            return self.render_to_response({'form': form})


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get(self, request, *args, **kwargs):
        if request.user.username != kwargs['user']:
            return redirect('profile', user=request.user.username)
        return super().get(request, *args, **kwargs)


activate_user = ActivateUserView.as_view()
deactivate_user = DeactivateUserView.as_view()
login = _LoginView.as_view()
logout = _LogoutView.as_view()
password_change = _PasswordChangeView.as_view()
password_change_done = _PasswordChangeDoneView.as_view()
password_reset = _PasswordResetView.as_view()
password_reset_complete = _PasswordResetCompleteView.as_view()
password_reset_confirm = _PasswordResetConfirmView.as_view()
password_reset_done = _PasswordResetDoneView.as_view()
profile = UserProfileView.as_view()
reactivate_user = ReactivateUserView.as_view()
signup = SignUpView.as_view()
