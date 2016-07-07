import json

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .bot import QuizBotMixin


class BotView(APIView, QuizBotMixin):

    def dispatch(self, request, *args, **kwargs):
        try:
            self.client_data

        except AttributeError:
            self.set_client(request.META['HTTP_FB_ID'])

        super(BotView, self).dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):

        incoming_message = json.loads(self.request.body.decode('utf-8'))

