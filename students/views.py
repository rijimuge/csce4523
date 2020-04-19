from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from .models import Student, Course, Enrollment
from .forms import StudentForm, CourseForm, EnrollmentForm, ListCoursesForm, ListEnrollmentsForm
import json


def index(request):
    template = loader.get_template('students/index.html')
    course_form = ListCoursesForm()
    enrollment_form = ListEnrollmentsForm()
    context = {
        'course_form': course_form,
        'enrollment_form': enrollment_form
    }
    return HttpResponse(template.render(context, request))


def list_students(request):
    student_list = Student.objects.all().values('student_id', 'student_name', 'major')
    template = loader.get_template('students/list_students.html')
    student_list_json = json.dumps(list(student_list), cls=DjangoJSONEncoder)
    context = {
        'student_list_json': student_list_json,
    }
    return HttpResponse(template.render(context, request))


def list_courses(request):
    if request.method == 'POST':
        form = ListCoursesForm(request.POST)
        if form.is_valid():
            dept_code = form.cleaned_data['dept_code']
            return HttpResponseRedirect('/students/list_courses_detail/' + dept_code)
    else:
        form = ListCoursesForm()

    return render(request, 'students/list_courses.html', {'form': form})


def list_courses_detail(request, dept_code_in):
    course_list = Course.objects.filter(dept_code__exact=dept_code_in).values('course_id', 'dept_code', 'course_num', 'title', 'credit_hours')
    template = loader.get_template('students/list_courses_detail.html')
    course_list_json = json.dumps(list(course_list), cls=DjangoJSONEncoder)
    context = {
        'course_list_json': course_list_json,
    }
    return HttpResponse(template.render(context, request))


def list_enrollments(request):
    if request.method == 'POST':
        form = ListEnrollmentsForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            return HttpResponseRedirect('/students/list_enrollments_detail/' + str(student_id))
    else:
        form = ListEnrollmentsForm()

    return render(request, 'students/list_enrollments.html', {'form': form})


def list_enrollments_detail(request, student_id):
    enrollment_list = Course.objects.filter(enrollment__student_id=student_id).values()
    template = loader.get_template('students/list_enrollments_detail.html')
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
                form = StudentForm()
                context = {
                    'error': True,
                    'form': form
                }
                return render(request, 'students/add_student.html', context)

            new_student = Student(student_id, student_name, major)
            new_student.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/students/list_students/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = StudentForm()

    return render(request, 'students/add_student.html', {'form': form})


def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course_id = form.cleaned_data['course_id']
            dept_code = form.cleaned_data['dept_code']
            course_num = form.cleaned_data['course_num']
            title = form.cleaned_data['title']
            credit_hours = form.cleaned_data['credit_hours']
            if Course.objects.filter(course_id__exact=course_id):
                print("Already exists")
                form = CourseForm()
                context = {
                    'error': True,
                    'form': form
                }
                return render(request, 'students/add_course.html', context)

            new_course = Course(course_id, dept_code, course_num, title, credit_hours)
            new_course.save()
            return HttpResponseRedirect('/students/list_courses_detail/' + dept_code)

    else:
        form = CourseForm()

    return render(request, 'students/add_course.html', {'form': form})


def add_enrollment(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment_id = form.cleaned_data['enrollment_id']
            student_id = form.cleaned_data['student_id']
            course_id = form.cleaned_data['course_id']
            if Enrollment.objects.filter(enrollment_id__exact=enrollment_id):
                print("Already exists")
                form = EnrollmentForm()
                context = {
                    'error1': True,
                    'form': form
                }
                return render(request, 'students/add_enrollment.html', context)
            elif not Course.objects.filter(course_id__exact=course_id):
                print("no such course")
                form = EnrollmentForm()
                context = {
                    'error2': True,
                    'form': form
                }
                return render(request, 'students/add_enrollment.html', context)
            elif not Student.objects.filter(student_id__exact=student_id):
                print("no such student")
                form = EnrollmentForm()
                context = {
                    'error3': True,
                    'form': form
                }
                return render(request, 'students/add_enrollment.html', context)

            new_enrollment = Enrollment(enrollment_id, student_id, course_id)
            new_enrollment.save()
            return HttpResponseRedirect('/students/list_enrollments_detail/' + str(student_id))

    else:
        form = EnrollmentForm()

    return render(request, 'students/add_enrollment.html', {'form': form})


