from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms
from boards.models import (
    Board, Topic, Post
)


class NewTopicForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )
    images = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True}), required=False)

    class Meta:
        model = Topic
        fields = ['subject', 'message', 'images']


class UpdateTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['subject', ]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]
