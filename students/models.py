from django.core.validators import MaxValueValidator
from django.db import models


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=18)
    major = models.CharField(max_length=18)

    def __str__(self):
        return self.student_name


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    dept_code = models.CharField(max_length=4)
    course_num = models.CharField(max_length=5)
    title = models.CharField(max_length=30)
    credit_hours = models.IntegerField(validators=[MaxValueValidator(6)])

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.student_id.student_name + " " + self.course_id.title
