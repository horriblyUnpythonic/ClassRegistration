from django.core.management.base import BaseCommand, CommandError

from student_registration.createstudentpref import get_preferences
from student_registration.models import CoursePreference
from student_registration.utils import assign_students


class Command(BaseCommand):
    help = 'add course pref from text file'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **kwargs):
        sp = get_preferences('student_registration/student-preferences.txt')

        student_assignments = assign_students(sp)
        print student_assignments
