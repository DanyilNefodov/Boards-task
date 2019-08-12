from django.contrib.auth import login as auth_login
from accounts.forms import ReaderSignUpForm, BloggerSignUpForm, LogInForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile as User
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView


class LogInView(LoginView):
    model = User
    form_class = LogInForm
    template_name = 'login.html'

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user,
                   backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')


def signup(request):
    return render(request, 'task_2_signup.html', {})


class ReaderSignUpView(CreateView):
    model = User
    form_class = ReaderSignUpForm
    template_name = 'task_2_signup_as.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Reader'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user,
                   backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')


class BloggerSignUpView(CreateView):
    model = User
    form_class = BloggerSignUpForm
    template_name = 'task_2_signup_as.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Blogger'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user,
                   backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')


@method_decorator(login_required, name='dispatch')
class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'my_account.html'
    success_message = 'Your account was updated successfully!'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user
