from .models import  Lesson, Question, Choice
from rest_framework.generics import ListAPIView
# from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import LessonSerializer, AnswerSerializer, QuizSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

class LessonListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class QuestionListView(ListAPIView):
    def get(self, request, lesson_id):
        if Lesson.objects.filter(number=lesson_id).exists():
            lesson = Lesson.objects.get(number=lesson_id)
            
            if Question.objects.filter(lesson_id=lesson).exists():
                questions = Question.objects.filter(lesson_id=lesson)
                
                res = []
                
                for item in questions.values():
                    question = Question.objects.get(id=item['id'])
                    choices = Choice.objects.defer('is_correct').filter(question=question)
                    item['choice'] = choices.values('id', 'question', 'choice_text')
                    res.append(item)

                data = {'questions': list(res)}

                return Response(data, status=200)
            else:
                return Response({
                    "message": "Sorry, this class does not have any questions."
                }, status=404)
        else:
            return Response({
                "message": "Sorry, this class does not exist."
            }, status=404)

class QuestionAddView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuizSerializer

    def post(self, request):
        serializer = QuizSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.save()
            lesson = data.get('lesson')
            question = data.get('question')
            choices = data.get('choices')

            lesson.save()
            question.save()
            for choice in choices:
                choice.save()

            return Response({"message": "Question added successfully"}, status=201)
        else:
            return Response(serializer.errors, status=400)

class ResultView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AnswerSerializer

    def post(self, request):
        serializer = AnswerSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.save()
            res = []
            total = 0

            for item in data:
                answers = item.get('choices')
                question_id = item.get('question')
                question = Question.objects.get(id=question_id)
                is_multi = question.is_multi
                choices = Choice.objects.filter(question=question).values()

                if is_multi:
                    count = 0
                    correct = 0
                    correct_answer = 0
                    incorrect_answer = 0

                    for choice in choices:
                        count += 1
                        if choice['is_correct']:
                            correct += 1
                            if choice['id'] in answers:
                                correct_answer += 1
                        else:
                            if choice['id'] in answers:
                                incorrect_answer += 1

                    temp = correct_answer * 10 / correct - incorrect_answer * 10 / count 
                    
                    score = max(0, temp)
                else:
                    score = 0
                    for choice in choices:
                        if choice['id'] in answers and choice['is_correct']:
                            score = 10
                            break

                res.append({
                    "question_id": question_id,
                    "score": round(score, 2)
                })
                total += score

            total /= len(data)

            return Response({
                "scores": res,
                "total": round(total, 2)
            }, status=200)
        else:
            return Response(serializer.errors, status=400)
