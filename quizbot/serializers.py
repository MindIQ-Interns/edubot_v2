from rest_framework.serializers import ModelSerializer

from .models import *


class BotUserSerializer(ModelSerializer):

    class Meta:
        model = BotUser


class SubjectSerializer(ModelSerializer):

    class Meta:
        model = Subject
        depth = 1


class TopicSerializer(ModelSerializer):

    class Meta:
        model = Topic


class QuestionSerializer(ModelSerializer):

    class Meta:
        model = Question