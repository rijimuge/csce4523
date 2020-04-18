from django import forms


class StudentForm(forms.Form):
    student_id = forms.IntegerField(label='Student ID', min_value=1)
    student_name = forms.CharField(label='Student name', max_length=18)
    major = forms.CharField(label='Major ', max_length=18)


class CourseForm(forms.Form):
    course_id = forms.IntegerField(label='Course ID', min_value=1)
    dept_code = forms.CharField(label='Department Code:', max_length=4)
    course_num = forms.CharField(label='Course Number', max_length=5)
    title = forms.CharField(label='Course Title', max_length=30)
    credit_hours = forms.IntegerField(label='Credit hours', max_value=6, min_value=1)


class EnrollmentForm(forms.Form):
    enrollment_id = forms.IntegerField(label='Student ID', min_value=1)
    student_id = forms.IntegerField(label='Student ID')
    course_id = forms.IntegerField(label='Course ID', min_value=1)
