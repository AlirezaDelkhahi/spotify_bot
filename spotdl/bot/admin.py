from django.contrib import admin

from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ['chat_id']


admin.site.register(Contact, ContactAdmin)
