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


def text_message(recipient_id, text):
    return {
        'recipient_id': recipient_id,
        'type': 'text',
        'text': text,
    }


def choice_message(recipient_id, question='', details='', choices=None, is_more=False):          # choices, a list of 2-tuples, where first value is the postback of the button, the second is the text on the button
    return {
        'recipient_id': recipient_id,
        'type': 'choice',
        'question': question,
        'details': details,
        'choices': choices if choices is not None else [],
        'is_more': is_more,
    }


def send(reply):
    for message in reply:
        pprint(message)


def send_error_message(recipient_id, text):
    message = text_message(recipient_id=recipient_id, text=text)
    send([message])


def send_question(recipient_id, question):
    options = Option.objects.all().filter(question=question)
    send([
        choice_message(recipient_id=recipient_id, question=question.text, details=question.details, choices=[(option.id, option.text) for option in options])
    ])


class QuizBotMixin:

    def __init__(self):
        self.client_data = self.mode = self.flag = self.subject = self.topic = self.quiz = self.question_number = self.answer_paper = None

    def set_client(self, fb_id):
        try:
            self.client_data = BotUser.objects.get(platform_id=fb_id)
            self.mode = 'choose_quiz'

        except BotUser.DoesNotExist:
            self.client_data = BotUser()
            self.mode = 'register'

        self.flag = {
            'set_first_name': False,
            'set_last_name': False,
            'set_username': False,
            'set_dob': False,
            'set_subject': False,
            'set_topic': False,
            'set_quiz': False,
            'get_next': False,
        }

        self.subject = None
        self.topic = None
        self.quiz = None
        self.question_number = None
        self.answer_paper = None
        
    def set_client_first_name(self, name):
        self.client_data.first_name = name
        self.flag['set_first_name'] = False
        
    def set_client_last_name(self, name):
        self.client_data.last_name = name
        self.flag['set_last_name'] = False
        
    def set_client_username(self, name):
        self.client_data.username = name
        self.flag['set_username'] = False
        
    def set_client_dob(self, dob):
        day = int(dob[:2])
        month = int(dob[3:5])
        year = int(dob[6:])
        self.client_data.dob = date(year=year, month=month, day=day)
        self.flag['set_dob'] = False

    def set_subject(self, subject):
        self.subject = subject
        self.flag['set_subject'] = False

    def set_topic(self, topic):
        self.topic = topic
        self.flag['set_topic'] = False

    def get_subjects(self, start_index=0):
        queryset = Subject.objects.all()
        return queryset

    def get_topics(self, start_index=0):
        queryset = Topic.objects.all().filter(subject=self.subject)
        return queryset

    def get_quizzes(self, start_index=0):
        queryset = Quiz.objects.all().filter(topics__id=self.topic)
        return queryset

    def find_score(self):
        answers = Answer.objects.all().filter(paper=self.answer_paper)
        score = 0

        for answer in answers:
            if answer.option.is_correct:
                score += 1

        return score

        
    def say_hi(self, recipient_id):
        reply = [
            text_message(recipient_id=recipient_id, text="Hey! I'm the Quizzer Bot!"),
        ]
        send(reply)
        
    def ask_for_first_name(self, recipient_id):
        reply = [
            text_message(recipient_id=recipient_id, text="What's your first name?"),
        ]
        send(reply)
        
    def ask_for_last_name(self, recipient_id):
        reply = [
            text_message(recipient_id=recipient_id, text="What's your last name?")
        ]
        send(reply)

    def ask_for_username(self, recipient_id):
        reply = [
            text_message(recipient_id=recipient_id, text="What would you like me to call you?")
        ]
        send(reply)

    def ask_for_dob(self, recipient_id):
        reply = [
            text_message(recipient_id=recipient_id, text="When were you born? (Reply in dd/mm/yyyy format)")
        ]
        send(reply)

    def send_list(self, recipient_id, queryset, is_more):
        reply = [
            choice_message(recipient_id=recipient_id, choices=queryset, is_more=is_more)
        ]
        send(reply)


    def set_client_data(self, received_message):
        if self.flag['set_first_name']:
            self.set_client_first_name(received_message['text'])

        elif self.flag['set_last_name']:
            self.set_client_last_name(received_message['text'])
            
        elif self.flag['set_username']:
            self.set_client_username(received_message['text'])
            
        elif self.flag['set_dob']:
            self.set_client_dob(received_message['text'])
            
    def check_client_data(self, received_message):
        recipient_id = received_message['sender_id']
        
        if self.client_data.first_name is None:
            self.flag['set_first_name'] = True
            self.say_hi(recipient_id)
            self.ask_for_first_name(recipient_id)

        elif self.client_data.last_name is None:
            self.flag['set_last_name'] = True
            self.ask_for_last_name(recipient_id)

        elif self.client_data.username is None:
            self.flag['set_username'] = True
            self.ask_for_username(recipient_id)

        elif self.client_data.dob is None:
            self.flag['set_dob'] = True
            self.ask_for_dob(recipient_id)

        else:
            self.mode = 'choose_quiz'
            self.check_quiz_data()

    def register(self, received_message):
        if received_message['type'] == 'raw':
            self.set_client_data(received_message)
            self.check_client_data(received_message)


    def set_quiz_data(self, received_message):
        if self.flag['set_subject']:
            self.set_subject(received_message['text'])

        if self.flag['set_topic']:
            self.set_topic(received_message['text'])

        if self.flag['set_quiz']:
            try:
                self.quiz = Quiz.objects.get(pk=int(received_message['text']))
                pprint(self.quiz)

            except Quiz.DoesNotExist:
                send_error_message(recipient_id=received_message['sender_id'], text='There was a problem: the requested quiz is not available right now.')

            self.question_number = 0

    def check_quiz_data(self, recipient_id, start_index=0):
        if self.subject is None:
            subjects = self.get_subjects(start_index=start_index)
            message = choice_message(recipient_id=recipient_id, choices=subjects)
            send([message])
            self.flag['set_subject'] = True

        elif self.topic is None:
            topics = self.get_topics(start_index=start_index)
            message = choice_message(recipient_id=recipient_id, choices=topics)
            send([message])
            self.flag['set_topic'] = True

        elif self.quiz is None:
            quizzes = self.get_quizzes(start_index=start_index)
            message = choice_message(recipient_id=recipient_id, choices=quizzes)
            send([message])
            self.flag['set_quiz'] = True

        else:
            self.mode = 'send_quiz'
            self.answer_paper = AttemptedPaper(student=self.client_data, quiz=self.quiz)
            self.send_question(recipient_id)

    def choose_quiz(self, received_message):
        if received_message['type'] == 'postback':
            if received_message['text'][:4] != 'more':
                self.set_quiz_data(received_message)
                self.check_quiz_data(received_message)

            else:
                self.check_quiz_data(received_message, start_index=int(received_message['text'][4:]))


    def update_answer_paper(self, received_message):
        answer = Answer(index=self.question_number, paper=self.answer_paper, option=received_message['text'])
        answer.save()

    def send_question(self, recipient_id):
        question = self.quiz.questions.all()[self.question_number]
        send_question(recipient_id=recipient_id, question=question)
        self.question_number += 1

    def conduct_quiz(self, received_message):
        if received_message['type'] == 'postback':
            self.update_answer_paper(received_message)

            try:
                self.send_question(recipient_id=received_message['sender_id'])

            except IndexError:
                score = self.find_score()
                StudentQuizReview(student=self.client_data, quiz=self.quiz, score=score).save()

                self.subject = self.topic = self.quiz = self.question_number = None
                self.mode = 'choose_quiz'
                self.check_quiz_data(received_message['sender_id'])

    def respond(self, received_message):
        if self.mode == 'register':
            self.register(received_message)

        elif self.mode == 'choose_quiz':
            self.choose_quiz(received_message)

        elif self.mode == 'send_quiz':
            self.conduct_quiz(received_message)