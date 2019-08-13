from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.edit import FormView
from django.shortcuts import redirect

from djangotask.forms import GenerateRandomBoardForm
from djangotask.tasks import create_random_boards


class GenerateRandomBoard(FormView):
    template_name = 'includes/form.html'
    form_class = GenerateRandomBoardForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_boards.delay(total)
        messages.success(
            self.request, 'We are generating your random boards! Wait a moment and refresh this page.')
        return redirect('home')
