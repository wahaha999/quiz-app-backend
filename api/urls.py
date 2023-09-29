from .views import LessonListView, QuestionListView, QuestionAddView, ResultView
from django.urls import path

app_name = "accounts"

urlpatterns = [
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('questions/<int:lesson_id>/', QuestionListView.as_view(), name='question-list'),
    path("submit-answers/", ResultView.as_view()),
    path('question/', QuestionAddView.as_view(), name='question-add'),
]