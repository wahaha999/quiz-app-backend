
from rest_framework import serializers

from .models import Question, Choice, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'question_text', 'choices', 'is_multi', 'lesson')
    
    # def create(self, validated_data):
    #     questions_data = validated_data.pop('questions')
    #     quiz = Quiz.objects.create(**validated_data)
    #     for question_data in questions_data:
    #         choices_data = question_data.pop('choices')
    #         question = Question.objects.create(quiz=quiz, **question_data)
    #         for choice_data in choices_data:
    #             Choice.objects.create(question=question, **choice_data)
    #     return quiz

class QuizSerializer(serializers.Serializer):
    lesson = serializers.IntegerField()
    question = serializers.CharField()
    is_multi = serializers.BooleanField()
    choice = serializers.ListField(child=serializers.DictField())

    def create(self, validated_data):
        # Custom logic to create an object based on the validated data
        # For example, you can create instances of Lesson, Question, and Choice models here
        lesson_data = validated_data['lesson']
        question_data = validated_data['question']
        is_multi = validated_data['is_multi']
        choice_data = validated_data['choice']

        if Lesson.objects.filter(number=lesson_data).exists():
            lesson = Lesson.objects.get(number=lesson_data)
        else:
            lesson = Lesson.objects.create(number=lesson_data)

        question = Question.objects.create(
            lesson=lesson,
            question_text=question_data,
            is_multi=is_multi
        )

        # Create choices and associate them with the question
        choices = []
        for choice_item in choice_data:
            choice = Choice.objects.create(
                question=question,
                **choice_item
            )
            choices.append(choice)

        # Return the created question object instance
        return {
            'lesson': lesson,
            'question': question,
            'choices': choices
        }


class OneAnswerSerializer(serializers.Serializer): 
    question=serializers.IntegerField()
    choices=serializers.ListField(
        child=serializers.IntegerField()
    )
            

class AnswerSerializer(serializers.Serializer): 
    answers = serializers.ListField(
        child=OneAnswerSerializer()
    )

    # choices = serializers.ListField(child=serializers.IntegerField())
    # question = serializers.IntegerField()

    def validate_answers(self, value):
        if not value:
            raise serializers.ValidationError("Answer choices cannot be empty.")
        return value

    def create(self, validated_data):
        answers_list = validated_data['answers']

        objects_list = []
        for answer in answers_list:
            question = answer['question']
            choices = answer['choices']
            object_data = {
                'question': question,
                'choices': choices
            }
            objects_list.append(object_data)

        return objects_list
