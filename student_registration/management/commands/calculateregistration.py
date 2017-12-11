from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from student_registration.createstudentpref import get_preferences
from student_registration.models import CoursePreference, Semester, Student, Course, CourseOffering, StudentRecord
from student_registration.utils import assign_students


class Command(BaseCommand):
    help = 'add calculate courses from student preferences'


    def handle(self, *args, **kwargs):
        example_sp = get_preferences('student_registration/student-preferences.txt')
        example_assignments = assign_students(example_sp)

        semester = Semester.objects.last()
        current_student_records = StudentRecord.objects.filter(course_offering__semester=semester)
        if current_student_records:
            for record in current_student_records:
                print record
            choice_given = raw_input('there are currently student records from this semester, stop, add, or delete?')
            if choice_given == 'delete':
                current_student_records.delete()
            elif choice_given == 'stop':
                print 'stopping'
                return
            elif choice_given == 'add':
                print 'whatever you way'
            else:
                print 'unrecognized'
                return


        cp = CoursePreference.objects.filter(semester=semester)
        sp = []
        for pref in cp:
            sp.append({
                'ordered-preference': pref.course_offering.values_list('id', flat=True),
                'max-classes': pref.max_classes,
                'student-credits': pref.student.total_credits,
                'student-id': pref.student_id,
            })

        assignments = assign_students(sp)
        for course_offering_id, student_id_list in assignments.iteritems():
            for student_id in student_id_list:
                sr = StudentRecord(student_id=student_id, course_offering_id=course_offering_id)
                sr.save()
