import string

from boards.models import Board
from django.utils.crypto import get_random_string

from celery import shared_task


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
