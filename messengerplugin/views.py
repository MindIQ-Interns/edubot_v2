import json, requests
from pprint import pprint

from django.views.generic import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from . import secrets


def text_message(recipient_id, text):
    return json.dumps({
        'recipient': {
            'id': recipient_id,
        },
        'message': {
            'text': text
        }
    })


def generic_template(recipient_id, title, subtitle, choices):
    return json.dumps({
        'recipient': {
            'id': recipient_id
        },
        'message': {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [
                        {
                            'title': title,
                            'subtitle': subtitle,
                            'buttons': [{
                                'type': 'postback',
                                'title': choice[1],
                                'payload': choice[0],
                            }]
                        } for choice in choices
                    ]
                }
            }
        }
    })


def raw_message(sender_id, text):
    return json.dumps({
        'sender_id': sender_id,
        'type': 'raw',
        'text': text
    })


def postback_message(sender_id, text):
    return json.dumps({
        'sender_id': sender_id,
        'type': 'postback',
        'text': text
    })


class BotInterface(View):

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))

        if incoming_message['type'] == 'text':
            status = requests.post(
                url=secrets.POST_MESSAGE_URL,
                headers={'Content-type: application/json'},
                data=text_message(recipient_id=incoming_message['recipient_id'], text=incoming_message['text'])
            )
            pprint(status.json())

        elif incoming_message['type'] == 'choice':
            status = requests.post(
                url=secrets.POST_MESSAGE_URL,
                headers={'Content-type: application/json', },
                data=generic_template(recipient_id=incoming_message['recipient_id'], title=incoming_message['question'], subtitle=incoming_message['details'], choices=incoming_message['choices'])
            )
            pprint(status.json())

        return HttpResponse()


class MessengerInterface(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(MessengerInterface, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == secrets.VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])

        else:
            return HttpResponse('Error, invalid token')

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))

        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    pprint(raw_message(sender_id=message['sender']['id'], text=message['message']['text']))

                elif 'postback' in message:
                    pprint(postback_message(sender_id=message['sender']['id'], text=message['postback']['payload']))

        return HttpResponse()
