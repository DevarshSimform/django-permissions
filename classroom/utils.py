from functools import wraps
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest
 

def object_permission_required(permission, model, lookup_field='id', obj_kwarg='pk'):
    """
    A decorator to check object-level permissions when only the object ID is passed.
    :param permission: The required permission (e.g., 'main.change_notice').
    :param model: The model class (e.g., Notice).
    :param lookup_field: The field name used to retrieve the object (default: 'id').
    :param obj_kwarg: The keyword argument name that holds the object ID (default: 'pk').
    """
    
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            obj_id = kwargs.get(obj_kwarg)  # Dynamically retrieve the object ID
            # If no object ID is provided, return a 400 Bad Request
            if obj_id is None:
                return HttpResponseBadRequest(f"Missing required parameter: {obj_kwarg}")
            # Fetch the object dynamically based on the lookup_field
            obj = get_object_or_404(model, **{lookup_field: obj_id})
            # Check if the user has permission on the object
            if not request.user.has_perm(permission, obj):
                raise PermissionDenied(f"You do not have permission to access this {model.__name__}.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

 