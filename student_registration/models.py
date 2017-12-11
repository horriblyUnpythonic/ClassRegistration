# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib

from django.contrib.auth.models import User
from django.db import models

from sortedm2m.fields import SortedManyToManyField

GRADES = (('A', 'A'),
          ('B', 'B'),
          ('C', 'C'),
          ('D', 'D'),
          ('F', 'F'),
          ('W', 'W'),
          ('drop', 'Dropped'),
          ('other', 'Other'),
          )


class Student(models.Model):
    user = models.OneToOneField(User)

    @property
    def total_credits(self):
        h = hashlib.md5(self.user.username)
        return int(h.hexdigest(), 16) % 30
        # cr = 0
        # for course in self.courses.filter(grade__isnull=False):
        #     cr += course.credits
        # return cr

    def __unicode__(self):
        return self.user.username

class Semester(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=64)
    credits = models.IntegerField()

    def __unicode__(self):
        return self.title


class CourseOffering(models.Model):
    course = models.ForeignKey(Course)
    semester = models.ForeignKey(Semester)
    # instructor = models.ForeignKey(User)

    def __unicode__(self):
        return u'{} - {}'.format(self.course, self.semester)


class StudentRecord(models.Model):
    course_offering = models.ForeignKey(CourseOffering)
    student = models.ForeignKey(Student, related_name='courses')
    grade = models.CharField(max_length=16, choices=GRADES, null=True)

    def __unicode__(self):
        return u'{} - {} - {}'.format(self.course_offering, self.student, self.grade)


class CoursePreference(models.Model):
    student = models.ForeignKey(Student)
    semester = models.ForeignKey(Semester)
    max_classes = models.IntegerField(default=1)

    course_offering = SortedManyToManyField(CourseOffering)

    def __unicode__(self):
        c = self.course_offering.count()
        word = 'course' if c == 1 else 'courses'
        return u'{} pref for {} - {} {}'.format(self.student.user, self.semester, c, word)

    class Meta:
        unique_together = (("student", "semester"),)
