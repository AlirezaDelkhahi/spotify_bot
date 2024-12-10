from django.db import models


class Contact(models.Model):
    chat_id = models.CharField(max_length=128, null=True, blank=True)
    user_id = models.CharField(max_length=128, null=True, blank=True)
