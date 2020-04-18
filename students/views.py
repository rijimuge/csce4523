from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from .models import Student, Course, Enrollment
from .forms import StudentForm
import json


def index(request):
    template = loader.get_template('students/index.html')
    return HttpResponse(template.render({}, request))


def list_students(request):
    student_list = Student.objects.all().values('student_id', 'student_name', 'major')
    template = loader.get_template('students/list_students.html')
    student_list_json = json.dumps(list(student_list), cls=DjangoJSONEncoder)
    context = {
        'student_list_json': student_list_json,
    }
    return HttpResponse(template.render(context, request))


def list_courses(request, dept_code_in):
    course_list = Course.objects.filter(dept_code__exact=dept_code_in).values('course_id', 'dept_code', 'course_num', 'title', 'credit_hours')
    template = loader.get_template('students/list_courses.html')
    course_list_json = json.dumps(list(course_list), cls=DjangoJSONEncoder)
    context = {
        'course_list_json': course_list_json,
    }
    return HttpResponse(template.render(context, request))


def list_enrollments(request, student_id):
    enrollment_list = Course.objects.filter(enrollment__student_id=student_id).values()
    template = loader.get_template('students/list_enrollments.html')
    enrollment_list_json = json.dumps(list(enrollment_list), cls=DjangoJSONEncoder)
    context = {
        'enrollment_list_json': enrollment_list_json,
    }
    return HttpResponse(template.render(context, request))


def add_student(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StudentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            student_name = form.cleaned_data['student_name']
            major = form.cleaned_data['major']
            if Student.objects.filter(student_id__exact=student_id):
                print("Already exists")
                context = {
                    'error': True,
                    'form': form
                }
                form = StudentForm()

                return render(request, 'students/add_student.html', context)
            newStudent = Student(student_id, student_name, major)
            newStudent.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/students/list_students/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = StudentForm()

    return render(request, 'students/add_student.html', {'form': form})
