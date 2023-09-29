from django.db import models

class Lesson(models.Model):
    number = models.IntegerField(default=1, unique=True)
    description = models.CharField(max_length=255, default="This is a classroom")

    def __str__(self):
        return str(self.number)

class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    is_multi = models.BooleanField(default=False)   # false: single choice, true: multi choice

    def __str__(self):
        return self.question_text
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text