from django.shortcuts import render, redirect, HttpResponse
from .forms import UserRegisterForm, NoticeForm
from django.contrib.auth.decorators import login_required, permission_required
from .models import Notice
from django.contrib import messages
from django.contrib.auth.models import User, Permission, Group
from django.core.exceptions import PermissionDenied
from .utils import object_permission_required


def home(request):
    return render(request, 'classroom/base.html')


@login_required
def notice_list(request):
    notices = Notice.objects.all()
    return render(request, 'classroom/notice_list.html', {'notices': notices})


@permission_required('classroom.add_notice', raise_exception=True)
def notice_create(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.author = request.user
            notice.save()
            return redirect('notice_list')
    else:
        form = NoticeForm()
    return render(request, 'classroom/notice_create.html', {'form': form})


# @permission_required('classroom.change_notice', raise_exception=True)
@object_permission_required('classroom.change_notice', Notice)
def notice_update(request, pk):
    notice = Notice.objects.get(pk=pk)


    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('notice_list')
    else:
        if notice.author == request.user or request.user.has_perm('classroom.change_notice'):
            form = NoticeForm(instance=notice)
        else:
            return redirect('notice_list')
    return render(request, 'classroom/notice_update.html', {'form': form})


@permission_required('classroom.delete_notice', Notice, raise_exception=True)
def notice_delete(request, pk):
    notice = Notice.objects.get(pk=pk)
    if notice.author == request.user or request.user.has_perm('classroom.delete_notice'):
        notice.delete()
    return redirect('notice_list')


def groups(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        group_id = request.POST.get('group')
        if group_id != "checker_flag":
            user = User.objects.get(pk=user_id)
            new_group = Group.objects.get(pk=group_id)
            user.groups.clear()
            user.groups.add(new_group)
        else:
            user = User.objects.get(pk=user_id)
            user.user_permissions.clear()
            permission_can_edit = Permission.objects.get(codename='view_notice')
            user.user_permissions.add(permission_can_edit)
            print(user.has_perm('view_notice'))


    if request.user.groups.filter(name='DB_admin').exists() or request.user.is_superuser:
        users = User.objects.all()
        groups = Group.objects.exclude(name='DB_admin')
        content = {
            'users': users,
            'groups': groups
        }
        return render(request, 'classroom/group.html', content)
    else:
        return redirect('notice_list')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserRegisterForm()
    return render(request, 'classroom/register.html', {'form': form})

