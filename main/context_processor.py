from .useradmin import UserStatus


def status(request):
    return {'status': UserStatus(request)}