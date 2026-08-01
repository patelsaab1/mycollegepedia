from django.urls import path, include

from .views import ExamListView,ExamRetrieveView,UpcomingExamRetrieveView,UpcomingExamListView,NotifyExamsAPIView

urlpatterns = [
    path('all-exam/',ExamListView.as_view(),name="all-exam"),
    path('exam/<str:slug>/',ExamRetrieveView.as_view(),name="exam"),
    path('all-upcoming-exam/',UpcomingExamListView.as_view(),name="all-upcoming-exam"),
    path('upcoming-exam/<str:slug>/',UpcomingExamRetrieveView.as_view(),name="upcoming-exam"),
    # Notify
    path('notify-exams/',NotifyExamsAPIView.as_view(),name="notify-exams"),
]
