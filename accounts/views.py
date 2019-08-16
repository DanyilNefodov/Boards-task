from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile as User
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from djangotask.celery.tasks import send_signup_invitation
from accounts.forms import (
    ReaderSignUpForm, BloggerSignUpForm, LogInForm, UserUpdateForm, AvatarForm
)


# def photo_list(request):
#     photos = Photo.objects.all()
#     if request.method == 'POST':
#         form = PhotoForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('photo_list')
#     else:
#         form = PhotoForm()
#     return render(request, 'album/photo_list.html', {'form': form, 'photos': photos})



class UserUpdateView(FormView):
    model = User
    form_class = UserUpdateForm
    template_name = 'my_account.html'

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()
        return redirect('home')


def crop_avatar_view(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('photo_list')
    else:
        form = AvatarForm()


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
        send_signup_invitation.delay(user.username, user.email)
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
        send_signup_invitation.delay(user.username, user.email)
        return redirect('home')
