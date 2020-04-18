from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list_students/', views.list_students, name='list_students'),
    path('add_student/', views.add_student, name='add_student'),
    path('list_courses/<str:dept_code_in>', views.list_courses, name='list_courses'),
    path('list_enrollments/<int:student_id>', views.list_enrollments, name='list_enrollments'),
]
