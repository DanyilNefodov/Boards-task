import string
from boards.models import Board
from django.utils.crypto import get_random_string
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def create_random_boards(total):
    for _ in range(total):
        name = 'Board {}'.format(get_random_string(10, string.ascii_letters))
        description = 'Description of {}'.format(name)
        Board.objects.create(
            name=name,
            description=description
        )
    return '{} random boards created with success!'.format(total)


@shared_task
def send_signup_invitation(username, email):
    send_mail('Welcome to Boards', 'Hello, {}!'.format(username), 'django.test.spamer@gmail.com',
              [email, ])
    return 'Invitation to {} was sended'.format(username)
