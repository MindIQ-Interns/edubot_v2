#from django.test import TestCase

# Create your tests here.
from quizbot.bot import *

b = QuizBotMixin()
b.set_client('1')

def m(t):
    return {'sender_id':'1', 'type':'postback', 'text':t}

b.choose_quiz(m('hi'))
b.choose_quiz(m('1'))
b.choose_quiz(m('1'))
b.choose_quiz(m('1'))