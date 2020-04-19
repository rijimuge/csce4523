from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list_students/', views.list_students, name='list_students'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_course/', views.add_course, name='add_course'),
    path('add_enrollment/', views.add_enrollment, name='add_enrollment'),
    path('list_courses/', views.list_courses, name='list_courses'),
    path('list_courses_detail/<str:dept_code_in>', views.list_courses_detail, name='list_courses_detail'),
    path('list_enrollments/', views.list_enrollments, name='list_enrollments'),
    path('list_enrollments_detail/<int:student_id>', views.list_enrollments_detail, name='list_enrollments_detail'),
]
