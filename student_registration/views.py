# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from logging import getLogger

# Create your views here.
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from student_registration import models
from student_registration.createstudentpref import get_preferences
from student_registration.models import Semester, CoursePreference, CourseOffering, Student, Course
from student_registration.utils import assign_students

logger = getLogger()


def get_student(view):
    user = view.request.user
    try:
        student = user.student
    except models.Student.DoesNotExist:
        logger.warning('Getting first student')
        student = models.Student.objects.first()
    return student


# class SelectStudent(TemplateView):
#     template_name = 'login.html'
#
#     def get_context_data(self, **kwargs):
#         students = Student.objects.all()
#
#         return {'students': students}
#         # return login_required({'semesters': semesters})


class SelectSemester(TemplateView):
    template_name = 'select-term.html'

    def get_context_data(self, **kwargs):
        # if not self.request.user.is_authenticated:
        #     return redirect('/login/')
        student = get_student(self)

        semesters = models.Semester.objects.all()
        return {'semesters': semesters}
        # return login_required({'semesters': semesters})


class RegisterForClass(TemplateView):
    template_name = 'register-for-class.html'

    def get_context_data(self, **kwargs):
        student = get_student(self)

        semester = Semester.objects.get(id=kwargs['semester'])
        course_offering = CourseOffering.objects.filter(semester=semester)
        course_preference, created = CoursePreference.objects.get_or_create(student=student, semester=semester)

        return {'course_offering': course_offering,
                'course_preference': course_preference.course_offering.all()
}

    def post(self, request, **kwargs):
        student = get_student(self)
        for data in request.POST.keys():
            print data, request.POST[data]
        # return redirect('/register/1')
        # return super(TemplateView, self).render_to_response(self.get_context_data())
        # c = self.get_context_data(**kwargs)
        return self.get(request, **kwargs)

# class Dumb(View):
#     def post(self, request):
#         for data in request.POST.keys():
#             print data, request.POST[data]
#         return redirect('/register/1')


class LoadReg(View):
    def get(self, request):
        sp = get_preferences('student_registration/student-preferences.txt')
        semester = Semester.objects.first()
        for student_p in sp:
            id = student_p['student-id']
            user, m1 = User.objects.get_or_create(id=id, username='auto{}'.format(id))
            student, m2 = Student.objects.get_or_create(user=user)
            # Add old courses in for credit count
            course_preferences = []
            for c in student_p['ordered-preference']:
                course, m3 = Course.objects.get_or_create(title=c, credits=3)
                offering = CourseOffering(course=course, semester=semester)
                course_preferences.append(offering)
            cp = CoursePreference.objects.get_or_create(student=student, semester=semester)

        return HttpResponse()


class RegAll(View):
    def get(self, request):
        semester = Semester.objects.first()
        sp = get_preferences('student_registration/student-preferences.txt')
        sp2 = []

        student_assignments = assign_students(sp)
        for pref in sp:
            student = Student.objects.get(user_id=pref['student-id'])
            sp2.append({
                'ordered-preference': student.coursepreference_set,
                'max-classes': 3,
                'student-credits': student.total_credits,
                'student-id': student.id,
            })
            print student_assignments
            student.coursepreference_set.get(semester=semester)

        return HttpResponse()
