# Generated by Django 2.2 on 2019-08-16 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0013_board_non_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='non_active',
        ),
        migrations.AddField(
            model_name='board',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]