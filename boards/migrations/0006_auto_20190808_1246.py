# Generated by Django 2.2 on 2019-08-08 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0005_auto_20190808_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='topic',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='log',
            name='user',
            field=models.CharField(max_length=255),
        ),
    ]