from django.contrib import sessions
from CityBikes import settings


class UserStatus:
    def __init__(self, request):
        self.session = request.session

        status = self.session.get(settings.USER_STATUS_SESSION_ID)

        if not status:
            status = self.session[settings.USER_STATUS_SESSION_ID] = 'user'

        self.status = status

    def change_status(self):

        if self.status == 'user':
            self.status = 'admin'
        else:
            self.status = 'user'

        self.save()

    def save(self):
        self.session.modified = True


