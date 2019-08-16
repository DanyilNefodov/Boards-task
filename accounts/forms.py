from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from PIL import Image
from nocaptcha_recaptcha.fields import NoReCaptchaField
from accounts.models import UserProfile as User
from accounts.models import (
    Reader, Blogger, Hobby, Interest, Avatar
)


class AvatarForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Avatar
        fields = ('file', 'x', 'y', 'width', 'height', )

    def save(self):
        photo = super(AvatarForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.file.path)


class UserUpdateForm(forms.Form):
    first_name = forms.CharField(
        required=False,
        max_length=255,
        help_text='The max length of the text is 255.'
    )
    last_name = forms.CharField(
        max_length=255,
        help_text='The max length of the text is 255.',
        required=False
    )
    email = forms.EmailField(required=False)
    avatar = forms.FileField(required=False)

    # @transaction.atomic
    # def save(self):
    #     user = super().save(commit=False)
    #     user.is_blogger = True
    #     user.save()
    #     blogger = Blogger.objects.create(
    #         user=user,
    #         birth_day=self.cleaned_data.get('birth_day'),
    #         country=self.cleaned_data.get('country')
    #     )
    #     blogger.hobbies.add(*self.cleaned_data.get('hobbies'))
    #     return user


class LogInForm():
    captcha = NoReCaptchaField()

    class Meta:
        model = User
        fields = ('username', 'password1')

    def confirm_login_allowed(self, user):
        if not user.is_active or not user.is_validated:
            raise forms.ValidationError(
                'There was a problem with your login.', code='invalid_login')


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True,
                            widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ReaderSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    status = forms.CharField(max_length=255)
    captcha = NoReCaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_reader = True
        user.save()
        reader = Reader.objects.create(
            user=user,
            status=self.cleaned_data.get('status')
        )
        reader.interests.add(*self.cleaned_data.get('interests'))
        return user


class BloggerSignUpForm(UserCreationForm):
    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    birth_day = forms.DateField()
    country = forms.CharField(max_length=255)
    captcha = NoReCaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_blogger = True
        user.save()
        blogger = Blogger.objects.create(
            user=user,
            birth_day=self.cleaned_data.get('birth_day'),
            country=self.cleaned_data.get('country')
        )
        blogger.hobbies.add(*self.cleaned_data.get('hobbies'))
        return user
