from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from board_app.forms import NewTopicForm
from board_app.models import (
    Board, Topic, Post
)


# Create your views here.


def home_view(request):
    board_list = Board.objects.all()

    context = {
        'boards': board_list,
    }
    return render(request, 'home_page.html', context)


def board_topics(request, pk):
    board = Board.objects.get(pk=pk)

    context = {
        'board': board
    }
    return render(request, 'board_topics.html', context)


def new_topic(request, pk):
    # return HttpResponse(pk)
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})
