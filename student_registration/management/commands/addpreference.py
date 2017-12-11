from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from student_registration.createstudentpref import get_preferences
from student_registration.models import CoursePreference, Semester, Student, Course, CourseOffering
from student_registration.utils import assign_students


class Command(BaseCommand):
    help = 'add course pref from text file'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **kwargs):
        sp = get_preferences('student_registration/student-preferences.txt')

        # student_assignments = assign_students(sp)
        # print student_assignments

        sp = get_preferences('student_registration/student-preferences.txt')
        semester = Semester.objects.last()
        for student_p in sp:
            id = student_p['student-id']
            un = 'auto{}'.format(id)
            user, m1 = User.objects.get_or_create(username=un)
            user.set_password(un)
            user.save()
            student, m2 = Student.objects.get_or_create(user=user)
            # Add old courses in for credit count
            course_preferences = []
            for c in student_p['ordered-preference']:
                course, m3 = Course.objects.get_or_create(title=c, credits=3)
                offering, m4 = CourseOffering.objects.get_or_create(course=course, semester=semester)
                offering.save()
                course_preferences.append(offering)
            cp, m5 = CoursePreference.objects.get_or_create(student=student, semester=semester)
            cp.course_offering = course_preferences
            cp.save()
