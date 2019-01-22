from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('CreateTest/', views.CreateTest.as_view(), name='create_test'),

    path('CreateQuestion/<int:pk>/', views.CreateQuestion.as_view(), name='create_question'),

    path('Testlist/', views.TestList.as_view(), name='test_list'),

    path('DeleteTest/<int:pk>/', views.DeleteTest.as_view(), name='delete_test'),

    path('TestView/<int:pk>/', views.TestDetail.as_view(), name='update_test'),

    path('DeleteQuestion/<int:pk>/', views.DeleteQuestion.as_view(), name='delete_question'),

    path('ExamAttempt/<int:test_id>/', views.ExamAttemptView.as_view(), name='exam_test'),

    path('PerformanceDetails/', views.PerformanceDetails.as_view(), name='performance_details'),

    path('TestPerformances/', views.TestDetail.as_view(), name='test_performances'),
]
