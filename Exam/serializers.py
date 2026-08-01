from rest_framework import serializers
from .models import Exam, UpcomingExam


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'


class SimpleExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        exclude = ('created_at', 'updated_at',)


class UpcomingExamSerializer(serializers.ModelSerializer):
    exam = SimpleExamSerializer(read_only=True)
    class Meta:
        model = UpcomingExam
        fields = '__all__'


class SimpleUpcomingExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpcomingExam
        exclude = ('created_at', 'updated_at',)


class AllExamSerializer(serializers.ModelSerializer):
    exam = SimpleExamSerializer(read_only=True)
    class Meta:
        model = UpcomingExam
        fields = '__all__'

# Notify
class NotifyExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ('id', 'slug', 'title', 'image','full_form',)