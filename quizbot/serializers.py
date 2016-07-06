from rest_framework.serializers import ModelSerializer, StringRelatedField, PrimaryKeyRelatedField

from .models import *


class BotUserSerializer(ModelSerializer):

    class Meta:
        model = BotUser


class SubjectSerializer(ModelSerializer):

    class NestedTopicSerializer(ModelSerializer):

        class Meta:
            model = Topic
            exclude = ('subject',)

    topics = NestedTopicSerializer(many=True, read_only=True)

    class Meta:
        model = Subject


class TopicSerializer(ModelSerializer):
    subject = StringRelatedField()

    class Meta:
        model = Topic


class QuestionSerializer(ModelSerializer):

    class NestedOptionSerializer(ModelSerializer):

        class Meta:
            model = Option
            fields = ('id', 'text', 'is_correct')

    options = NestedOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'details', 'review', 'options')


class OptionSerializer(ModelSerializer):

    class Meta:
        model = Option
        fields = ('id', 'text', 'is_correct', 'question')
        depth = 1


class QuizSerializer(ModelSerializer):
    topics = PrimaryKeyRelatedField(many=True, read_only=True)
    questions = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Quiz


class AnswerSerializer(ModelSerializer):

    class Meta:
        model = Answer
        depth = 1


class AttemptedPaperSerializer(ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = AttemptedPaper
