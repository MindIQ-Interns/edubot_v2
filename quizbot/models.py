from django.db import models


class BotUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    dob = models.DateTimeField()
    gender = models.CharField(max_length=1)
    platform_id = models.CharField(max_length=150)
    on_portal = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject)

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField()
    details = models.TextField(null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    # TODO: Add difficulty field

    def __str__(self):
        return self.text


class Option(models.Model):
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question)

    def __str__(self):
        return self.text


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100, default='Anonymous')
    author_id = models.IntegerField(null=True, blank=True)
    created_on = models.DateTimeField()
    submission_deadline = models.DateTimeField(null=True, blank=True)
    topics = models.ManyToManyField(Topic)
    questions = models.ManyToManyField(Question)
    # TODO: Add is_uniform field
    is_important = models.BooleanField(default=False)
    max_score = models.IntegerField()

    def __str__(self):
        return self.name

    def length(self):
        return len(self.questions)


class AttemptedPaper(models.Model):
    student = models.ForeignKey(BotUser)
    quiz = models.ForeignKey(Quiz)
    attempted_till = models.IntegerField(default=0)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.quiz.__str__() + ', ' + self.student.__str__()


class Answer(models.Model):
    index = models.IntegerField()
    paper = models.ForeignKey(AttemptedPaper)
    option = models.ForeignKey(Option)

    def __str__(self):
        return self.option.__str__()


class StudentQuizReview(models.Model):
    student = models.ForeignKey(BotUser)
    quiz = models.ForeignKey(Quiz)
    score = models.IntegerField()
    details = models.TextField(null=True, blank=True)
