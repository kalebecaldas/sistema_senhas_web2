# app/auth_utils.py
from functools import wraps
from flask_login import current_user
from flask import abort

def role_required(*roles):
    """Permite a rota somente se current_user.tipo estiver em roles."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.tipo not in roles:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator
