import json

from django.views.generic import View
from django.http import HttpResponse

from .models import *
from .bot import QuizBotMixin


class BotView(View, QuizBotMixin):

    def dispatch(self, request, *args, **kwargs):
        try:
            self.client_data

        except AttributeError:
            self.set_client(request.META['HTTP_SENDER_ID'])

        super(BotView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        self.respond(incoming_message)

