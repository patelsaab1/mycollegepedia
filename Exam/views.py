from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, ListAPIView
from Exam.serializers import ExamSerializer, SimpleExamSerializer, UpcomingExamSerializer, SimpleUpcomingExamSerializer, \
    AllExamSerializer,NotifyExamSerializer
from Exam.models import Exam, UpcomingExam
from django.utils import timezone
from datetime import timedelta
from django.db import models

# Create your views here.
class ExamListView(ListAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer


class ExamRetrieveView(RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    lookup_field = 'slug'


class UpcomingExamListView(ListAPIView):
    queryset = UpcomingExam.objects.all()
    serializer_class = UpcomingExamSerializer


class UpcomingExamRetrieveView(RetrieveAPIView):
    queryset = UpcomingExam.objects.all()
    serializer_class = AllExamSerializer
    lookup_field = 'slug'

# Notify
class NotifyExamsAPIView(ListAPIView):
    serializer_class = NotifyExamSerializer

    def get_queryset(self):
        today = timezone.now()
        start_of_week = today - timedelta(days=today.weekday())

        queryset = Exam.objects.filter(
            models.Q(created_at__gte=start_of_week) |
            models.Q(updated_at__gte=start_of_week)
        )
        return queryset
