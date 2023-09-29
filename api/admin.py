from .models import Lesson, Question, Choice
from django.contrib import admin

# Register your models here.
admin.site.register(Lesson)
admin.site.register(Question)
admin.site.register(Choice)