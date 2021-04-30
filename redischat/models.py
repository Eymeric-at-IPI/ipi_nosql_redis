from datetime import datetime
from django.db import models
from django.conf import settings as django_settings

DB_REDIS = django_settings.DB_REDIS


# TODO : ajouter lez fonction bdd au model
class Message(models.Model):
    username = models.CharField(max_length=64)
    room = models.CharField(max_length=64)
    content = models.TextField()
    send_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('send_date',)


class RedisDB:

    def __init__(self, name):
        self.tmp_var = "hello from DB class"

    def says_hello(self):
        print(self.tmp_var)


class RedisMessage:

    def __init__(self, sender, content, room):
        self.sender = sender
        self.content = content
        self.room = room
        self.send_date = datetime.now()

    def save(self):
        DB_REDIS.set(f"{self.room}_{self.sender}", self.content)


