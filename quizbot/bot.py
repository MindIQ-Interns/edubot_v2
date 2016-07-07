from pprint import pprint
from datetime import date

from .models import *


# Requires data of the form:
#
# {
#    'sender_id': <sender fb id>,
#    'type': <'raw'/'postback'>,
#    'text': <data>
# }


def message(recipient_id, message_type, text):
    return {
        'recipient_id': recipient_id,
        'type': message_type,
        'text': text,
    }


def send(reply):
    for message in reply:
        pprint(message)


class QuizBotMixin:

    def set_client(self, fb_id):
        try:
            self.client_data = BotUser.objects.get(platform_id=fb_id)
            self.mode = 'home'

        except BotUser.DoesNotExist:
            self.client_data = BotUser()
            self.mode = 'register'

        self.flag = {
            'set_first_name': False,
            'set_last_name': False,
            'set_username': False,
            'set_dob': False,
        }

    def set_data(self, received_message):
        if self.flag['set_first_name']:
            self.client_data.first_name = received_message['text']
            self.flag['set_first_name'] = False

        elif self.flag['set_last_name']:
            self.client_data.last_name = received_message['text']
            self.flag['set_last_name'] = False

        elif self.flag['set_username']:
            self.client_data.username = received_message['text']
            self.flag['set_username'] = False

        elif self.flag['set_dob']:
            day = int(received_message['text'][:2])
            month = int(received_message['text'][3:5])
            year = int(received_message['text'][6:])
            self.client_data.dob = date(year=year, month=month, day=day)
            self.flag['set_dob'] = False

    def check_data(self, received_message):
        if self.client_data.first_name is None:
            self.flag['set_first_name'] = True
            reply = [
                message(recipient_id=received_message['sender_id'], message_type='raw', text="Hey! I'm the Quizzer Bot!"),
                message(recipient_id=received_message['sender_id'], message_type='raw', text="What's your first name?"),
            ]
            send(reply)

        elif self.client_data.last_name is None:
            self.flag['set_last_name'] = True
            reply = [message(recipient_id=received_message['sender_id'], message_type='raw', text="What's your last name?")]
            send(reply)

        elif self.client_data.username is None:
            self.flag['set_username'] = True
            reply = [message(recipient_id=received_message['sender_id'], message_type='raw', text="What would you like me to call you?")]
            send(reply)

        elif self.client_data.dob is None:
            self.flag['set_dob'] = True
            reply = [message(recipient_id=received_message['sender_id'], message_type='raw', text="When were you born? (Reply in dd/mm/yyyy format)")]
            send(reply)

        else:
            self.mode = 'home'

    def register(self, received_message):
        self.set_data(received_message)
        self.check_data(received_message)