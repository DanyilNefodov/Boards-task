# Generated by Django 2.2 on 2019-08-14 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0007_auto_20190808_1317'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('file', models.FileField(upload_to='photos/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
