from django.contrib import admin

from quizbot.models import *


models = [BotUser, Subject, Topic, Question, Option, Quiz, AttemptedPaper, Answer, StudentQuizReview]

for model in models:
    admin.site.register(model)