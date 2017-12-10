# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
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


class Home(TemplateView):
    template_name = 'home.html'

def get_student(view):
    user = view.request.user
    try:
        student = user.student
    except models.Student.DoesNotExist:
        logger.warning('Getting first student')
        student = models.Student.objects.first()
    return student


class SelectSemester(TemplateView):
    template_name = 'select-term.html'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('/login/')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
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

    def post(self, request,  **kwargs):
        student = get_student(self)
        courses = []
        for data in request.POST.keys():
            m = re.match('course_id-(\d+)', data)
            order_value = request.POST[data]
            if m:
                if order_value:
                    co = CourseOffering.objects.get(id=m.groups()[0])
                    courses.append((int(order_value), co))
        sorted_pref = [i[1] for i in sorted(courses)]
        semester = Semester.objects.get(id=kwargs['semester'])
        course_preference = CoursePreference.objects.get(student=student, semester=semester)
        course_preference.course_offering = sorted_pref
        # return redirect('/register/1')
        # return super(TemplateView, self).render_to_response(self.get_context_data())
        # c = self.get_context_data(**kwargs)
        return self.get(request, **kwargs)
