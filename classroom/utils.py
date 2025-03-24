from functools import wraps
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest

def object_permission_required(permission, model, lookup_field='id', obj_kwarg='pk'):
    """
    A decorator to check object-level permissions when only the object ID is passed.
    - Professors, Principals, and DB_admins can edit any notice.
    - Students can only edit their own notices.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            obj_id = kwargs.get(obj_kwarg)
            if obj_id is None:
                return HttpResponseBadRequest(f"Missing required parameter: {obj_kwarg}")

            obj = get_object_or_404(model, **{lookup_field: obj_id})

            # Groups that have full edit access
            privileged_groups = {'Professor', 'Principal', 'DB_admin'}
            if request.user.groups.filter(name__in=privileged_groups).exists():
                return view_func(request, *args, **kwargs)

            # Students can only edit their own notices
            if request.user.groups.filter(name='Student').exists():
                if obj.author == request.user or request.user.has_perm(permission, obj):
                    print(f"User {request.user} is editing their own notice.")
                    return view_func(request, *args, **kwargs)
                else:
                    raise PermissionDenied("You can only edit your own notices.")

            # Default permission check if not in predefined groups
            if not request.user.has_perm(permission, obj):
                raise PermissionDenied(f"You do not have permission to edit this {model.__name__}.")

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator