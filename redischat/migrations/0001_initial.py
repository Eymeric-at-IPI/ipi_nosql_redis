# Generated by Django 3.2 on 2021-04-22 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('room', models.CharField(max_length=64)),
                ('content', models.TextField()),
                ('send_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('send_date',),
            },
        ),
    ]
