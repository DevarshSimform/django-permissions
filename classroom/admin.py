from django.contrib import admin
from .models import Notice
from guardian.admin import GuardedModelAdmin

@admin.register(Notice)
class NoticeAdmin(GuardedModelAdmin):
    list_display = ('title', 'content', 'date_posted', 'author')

