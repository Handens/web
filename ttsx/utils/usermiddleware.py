from _datetime import datetime
import re

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.deprecation import MiddlewareMixin

from users.models import UserTicket


class UserAutherMiddleware(MiddlewareMixin):
    def process_request(self, request):
        paths = ['/user/login/', '/user/register/']

        for path in paths:
            if re.match(path, request.path):
                return None

        cookies = request.COOKIES.get('ticket')

        if not cookies:
            return HttpResponseRedirect(reverse('user:login'))

        user = UserTicket.objects.filter(ticket=cookies).first()

        if not user:
            return HttpResponseRedirect(reverse('user:login'))

        if user.out_time.replace(tzinfo=None) < datetime.now():
            user.delete()
            return HttpResponseRedirect(reverse('user:login'))

        request.user = user.ttsx_user
