from django.contrib.auth import login as auth_login
from accounts.forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from djangotask.settings import AUTH_USER_MODEL as User
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView
from django.utils.decorators import method_decorator
# from accounts.forms import (
#     ReaderSignUpForm
# )

# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# class ReaderSignUpView(CreateView):
#     model = User
#     form_class = ReaderSignUpForm
#     template_name = 'signup.html'
#
#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'Reader'
#         return super().get_context_data(**kwargs)
#
#     def form_valid(self, form):
#         user = form.save()
#         auth_login(self.request, user)
#         return redirect('readers:quiz_list')


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'my_account.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user
