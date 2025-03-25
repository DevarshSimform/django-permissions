from django.shortcuts import render, redirect, HttpResponsePermanentRedirect
from .forms import UserRegisterForm, NoticeForm
from django.contrib.auth.decorators import login_required, permission_required
from .models import Notice
from django.contrib import messages
from django.contrib.auth.models import User, Permission, Group
from django.core.exceptions import PermissionDenied
from .utils import object_permission_required
from guardian.shortcuts import assign_perm, remove_perm


def home(request):
    return render(request, 'classroom/base.html')


# @login_required
def notice_list(request):
    notices = Notice.objects.order_by('-date_posted')
    return render(request, 'classroom/notice_list.html', {'notices': notices})


@login_required
def assign_notice(request):
    if request.method == 'POST':
        notice_id = request.POST.get('notice')
        user_id = request.POST.get('user')
        is_assign = request.POST.get('action')
        notice = Notice.objects.get(id=notice_id)
        user = User.objects.get(id=user_id)
        if is_assign == 'assign':
            assign_perm('classroom.change_notice', user, notice)
        else:
            remove_perm('classroom.change_notice', user, notice)
        return redirect('notice_list')
    else:
        users = User.objects.all()
        notices = Notice.objects.filter(author = request.user)
        content = {
                'users': users, 
                'notices': notices
            }
    return render(request, 'classroom/assign_notice.html', content)


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
        form = NoticeForm(instance=notice)
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

        user = User.objects.get(pk=user_id)
        new_group = Group.objects.get(pk=group_id)
        user.groups.clear()
        user.groups.add(new_group)


    if request.user.groups.filter(name='DB_admin').exists() or request.user.is_superuser:
        users = User.objects.all()
        groups = Group.objects.exclude(name='DB_admin')
        content = {
            'users': users,
            'groups': groups
        }
        return render(request, 'classroom/group.html', content)
    else:
        # return redirect('notice_list')
        return redirect("notice_list", permanent=True)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserRegisterForm()
    return render(request, 'classroom/register.html', {'form': form})



# Implemented custom file response

# from django.http import FileResponse

# def file_response(request):
#     file_path = '/home/devarsh.chhatrala@simform.dom/Desktop/django-permissions-classroom/classroom/test.pdf'
#     response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
#     response['content Disposition'] = 'attachment; filename=download.pdf'
#     return response

