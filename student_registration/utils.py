from __future__ import division
from collections import defaultdict
from operator import itemgetter

from createstudentpref import get_preferences


def assign_students(student_prefs):
    registration_list = defaultdict(list)
    for student_record in student_prefs:
        student_id = student_record['student-id']
        student_credits = student_record['student-credits']
        ordered_preference = student_record['ordered-preference']
        num_classes = len(ordered_preference)
        max_classes = student_record['max-classes']
        for i, class_name in enumerate(ordered_preference):
            wait_list = registration_list[class_name]
            preference_score = student_credits / max_classes / num_classes / (i + 1)
            wait_list.append((preference_score, student_id))

    for k in registration_list:
        registration_list[k].sort(reverse=1)

    # return dict(registration_list)

    remaining_classes = True
    # rejected_classes = []

    final_registration = {k: [] for k in registration_list}

    student_lookup = {s['student-id']: dict({'registered': []}, **s) for s in student_prefs}
    while remaining_classes:
        remaining_classes = False
        for course, v in registration_list.items():
            if v:
                remaining_classes = True
                score, student_id = v.pop(0)

                s = student_lookup[student_id]
                under_max = len(s['registered']) < s['max-classes']

                if len(final_registration[course]) < 15 and under_max:
                    student_lookup[student_id]['registered'].append(course)
                    final_registration[course].append(student_id)

    for s in sorted(student_lookup.values(), key=itemgetter('student-credits')):
        print '--'
        print 'regi', s['registered']
        print 'pref', s['ordered-preference']
        print 'cred', s['student-credits']
        print 'maxc', s['max-classes']
        print 's id', s['student-id']

    return final_registration


if __name__ == '__main__':
    sp = get_preferences('student-preferences.txt')

    student_assignments = assign_students(sp)
    print student_assignments

    # print '\n\n'
    # for c, l in student_assignments.items():
    #     print c, l



