from functools import wraps

from django.shortcuts import redirect


def login_required(view_func):
    @wraps(view_func)
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated:
            return redirect('member:login')
        return view_func(*args, **kwargs)
    return decorator
