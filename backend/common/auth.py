from django.contrib.auth import (
    BACKEND_SESSION_KEY,
    HASH_SESSION_KEY,
    SESSION_KEY,
    _get_backends,
    _get_user_session_key,
    user_logged_in,
)
from django.middleware.csrf import rotate_token
from django.utils.crypto import constant_time_compare


def custom_login(request, user, backend=None):
    """Меняет хэш для PhoneBackend"""
    session_auth_hash = ""
    if user is None:
        user = request.user
    if hasattr(user, "get_session_auth_hash"):
        if backend == "users.backends.PhoneBackend":
            session_auth_hash = user.get_session_auth_hash(phone=True)
        else:
            session_auth_hash = user.get_session_auth_hash()
    if SESSION_KEY in request.session:
        if _get_user_session_key(request) != user.pk or (
            session_auth_hash
            and not constant_time_compare(
                request.session.get(HASH_SESSION_KEY, ""), session_auth_hash
            )
        ):
            request.session.flush()
    else:
        request.session.cycle_key()

    try:
        backend = backend or user.backend
    except AttributeError:
        backends = _get_backends(return_tuples=True)
        if len(backends) == 1:
            _, backend = backends[0]
        else:
            raise ValueError(
                "You have multiple authentication backends configured and "
                "therefore must provide the `backend` argument or set the "
                "`backend` attribute on the user."
            )
    else:
        if not isinstance(backend, str):
            raise TypeError("backend must be a dotted import path string (got %r)." % backend)

    request.session[SESSION_KEY] = user._meta.pk.value_to_string(user)
    request.session[BACKEND_SESSION_KEY] = backend
    request.session[HASH_SESSION_KEY] = session_auth_hash
    if hasattr(request, "user"):
        request.user = user
    rotate_token(request)
    user_logged_in.send(sender=user.__class__, request=request, user=user)
