# Generated by Django 2.2 on 2019-08-16 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0011_auto_20190814_1454'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'verbose_name': 'photo', 'verbose_name_plural': 'photos'},
        ),
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(null=True, upload_to='photos/'),
        ),
    ]