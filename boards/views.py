from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile as User
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, ListView
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from django.utils import timezone
from django.db.models import Count
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import humanize
import datetime
import json
import csv
import xlwt
from django.views.generic.edit import FormView
from weasyprint import HTML
from boards.forms import (
    NewTopicForm, PostForm, UpdateTopicForm
)
from boards.models import (
    Board, Topic, Post, Log
)
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail import send_mail
from djangotask.celery.tasks import send_reply_notification


# Create your views here.


def send_mail_view(request):
    send_mail('subject', 'body of the message', 'django.test.spamer@gmail.com',
              ['django.test.spamer@gmail.com', ])
    return HttpResponse('Sended')
    # except:
    #     return HttpResponse('Not sended')


def home_view(request):
    board_list = Board.objects.order_by('-id')
    logs = Log.objects.order_by('-id')[:10]
    page = request.GET.get('page', 1)
    paginator = Paginator(board_list, 20)

    try:
        boards = paginator.page(page)
    except PageNotAnInteger:
        boards = paginator.page(1)
    except EmptyPage:
        boards = paginator.page(paginator.board_pages)

    return render(request, 'home_page.html', {'boards': boards, 'logs': logs})


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
        queryset = self.board.topics.order_by(
            '-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


@login_required
def new_topic(request, pk):
    print('ffffffffff')
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
        Log.objects.create(
            topic=topic.subject,
            kind=0,
            user=request.user
        )
        messages.success(
            request, 'Your topic was created successfully!', extra_tags='alert')
        return redirect('topic_posts', pk=pk, topic_pk=topic.pk)  # <- here
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def update_topic(request, pk, topic_pk):
    data = dict()
    if request.method == 'POST':
        form = UpdateTopicForm(request.POST)
        if form.is_valid():
            topic = get_object_or_404(Topic, pk=topic_pk)
            topic.subject = form.cleaned_data['subject']
            topic.last_updated = timezone.now()
            topic.save()
            Log.objects.create(
                topic=topic.subject,
                kind=1,
                user=request.user
            )
            data['form_is_valid'] = True
            data['board_pk'] = pk
            data['topic_pk'] = topic_pk
            data['naturaldelta'] = humanize.naturaldelta(
                datetime.datetime.now())
            messages.success(
                request, 'Your topic was updated successfully!', extra_tags='alert')
        else:
            data['form_is_valid'] = False

    context = {
        'form': form,
        'board_pk': pk,
        'topic_pk': topic_pk
    }

    data['html_form'] = render_to_string(
        template_name='includes/partial_update.html',
        context=context,
        request=request,
    )
    return JsonResponse(data)


def delete_topic(request, pk, topic_pk, confirmed=False):
    data = dict()

    if request.method == 'POST':
        if confirmed:
            topic = Topic.objects.get(pk=topic_pk)
            Post.objects.filter(topic=topic).delete()
            Log.objects.create(
                topic=topic.subject,
                kind=2,
                user=request.user
            )
            topic.delete()
            data['board_pk'] = pk,
            data['topic_pk'] = topic_pk
            data['confirmed'] = True
            messages.success(
                request, 'Your topic was deleted successfully!', extra_tags='alert')

    context = {
        'board_pk': pk,
        'topic_pk': topic_pk
    }

    data['html_form'] = render_to_string(
        template_name='includes/partial_delete.html',
        context=context,
        request=request,
    )
    return JsonResponse(data)


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
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get(
            'pk'), pk=self.kwargs.get('topic_pk'))
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

        topic_url = reverse('topic_posts', kwargs={
                            'pk': pk, 'topic_pk': topic_pk})
        topic_post_url = '{url}?page={page}#{id}'.format(
            url=topic_url,
            id=post.pk,
            page=topic.get_page_count()
        )
        send_reply_notification.delay(
            post.topic.starter.username,
            post.topic.starter.email,
            post.topic.subject,
            post.created_by.username
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


def put_in_boards(request, boards_, topics_, posts_):
    try:
        from_ = (Board.objects.order_by('-pk')[0].id + 1)
    except:
        from_ = 1
    for i in range(from_, from_ + int(boards_)):
        board = Board.objects.create(
            name='Board #{0}'.format(i),
            description='Description #{0}'.format(i)
        )
        for j in range(from_, from_ + int(topics_)):
            topic = Topic.objects.create(
                subject='Subject #{0}'.format(j),
                starter=request.user,
                board=board,
                views=0
            )
            for k in range(from_, from_ + int(posts_)):
                Post.objects.create(
                    message='Message #{0}'.format(k),
                    topic=topic,
                    created_by=request.user
                )
    return HttpResponse('Completed')


def export_posts_csv(request, pk, topic_pk):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="posts.csv"'

    writer = csv.writer(response)
    writer.writerow(['Message', 'Created by'])

    posts = Post.objects.filter(topic=topic_pk).values_list(
        'message', 'created_by')
    for post in posts:
        writer.writerow(post)

    return response


def export_posts_xlwt(request, pk, topic_pk):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="posts.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Posts')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Message', 'Created by', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Post.objects.filter(topic=topic_pk).values_list(
        'message', 'created_by')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_posts_pdf(request, pk, topic_pk):
    topic = Topic.objects.get(id=topic_pk)
    posts = Post.objects.filter(topic=topic_pk)
    html_string = render_to_string(
        'topic_posts.html', {'posts': posts, 'topic': topic})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf')

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

    return response
