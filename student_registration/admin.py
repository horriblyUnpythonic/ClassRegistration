# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from student_registration import models

admin.site.register(models.Student)
admin.site.register(models.Course)
admin.site.register(models.CourseOffering)
admin.site.register(models.CoursePreference)
admin.site.register(models.StudentRecord)
admin.site.register(models.Semester)
