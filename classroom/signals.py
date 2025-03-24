from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Notice
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

@receiver(post_save, sender=User)
def default_user_role(sender, instance, created, **kwargs):
    if created:
        user = instance
        default_group = Group.objects.get(name='Student')
        user.groups.add(default_group)

@receiver(post_save, sender=Notice)
def user_can_change_own_notice(sender, instance, created, **kwargs):
    if created:
        notice = instance
        user = notice.author
        assign_perm('change_notice', user, notice)
