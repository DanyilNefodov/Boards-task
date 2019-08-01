from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile as User
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, ListView
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from board_app.forms import (
    NewTopicForm, PostForm
)
from board_app.models import (
    Board, Topic, Post
)


# Create your views here.


def home_view(request):
    board_list = Board.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(board_list, 20)

    try:
        boards = paginator.page(page)
    except PageNotAnInteger:
        boards = paginator.page(1)
    except EmptyPage:
        boards = paginator.page(paginator.board_pages)

    return render(request, 'home_page.html', {'boards': boards})


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    form = NewTopicForm(request.POST)
    if form.is_valid():
        topic = form.save(commit=False)
        topic.board = board
        topic.starter = request.user  # <- here
        topic.save()
        Post.objects.create(
            message=form.cleaned_data.get('message'),
            topic=topic,
            created_by=request.user  # <- and here
        )
        return redirect('topic_posts', pk=pk, topic_pk=topic.pk)  # <- here
    return render(request, 'new_topic.html', {'board': board, 'form': form})


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)  # <-- here
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True  # <-- until here

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.topic = topic
        post.created_by = request.user
        post.save()

        topic.last_updated = timezone.now()
        topic.save()

        topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
        topic_post_url = '{url}?page={page}#{id}'.format(
            url=topic_url,
            id=post.pk,
            page=topic.get_page_count()
        )
        return redirect(topic_post_url)
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


def put_in_boards(request):
    from_ = Board.objects.order_by('-pk')[0].id + 1
    plus_ = 10
    for i in range(from_, from_ + plus_):
        board = Board.objects.create(
            name='Board #{0}'.format(i),
            description='Description #{0}'.format(i)
        )
        for j in range(from_, from_ + plus_):
            topic = Topic.objects.create(
                subject='Subject #{0}'.format(j),
                starter=request.user,
                board=board,
                views=0
            )
            for k in range(from_, from_ + plus_):
                Post.objects.create(
                    message='Message #{0}'.format(j),
                    topic=topic,
                    created_by=request.user
                )
    return HttpResponse('Completed')
