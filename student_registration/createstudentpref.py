import json
import random
from collections import defaultdict


def randomize_preferences():
    classes = [(8, 'super sweet'),
               (5, 'everyone needs'),
               (4, 'fun class'),
               (3, 'boring prereq'),
               (2, 'hard class'),
               (1, 'boring ancillary'),
               ]

    total = sum(x for x, y in classes)

    students = []
    for s in range(100):
        ordered_preference = []
        while 1:
            if random.random() > .7:
                break
            r = random.uniform(0, total)
            up_to = 0
            for w, c in classes:
                up_to += w
                if c in ordered_preference:
                    continue
                if up_to >= r:
                    ordered_preference.append(c)
                    break
            if len(ordered_preference) > 3:
                break

        if ordered_preference:
            students.append({
                'ordered-preference': ordered_preference,
                'student-credits': random.randint(0, 40),
                'student-id': s,
                'max-classes': random.randint(1, len(ordered_preference)),
            })
    return students


def write_preferences(sp):
    with open('student-preferences.txt', 'w') as fid:
        json.dump(sp, fid, indent=2)


def get_preferences(file_name):
    with open(file_name) as fid:
        return json.load(fid)


if __name__ == '__main__':

    # write_preferences(randomize_preferences())

    t = 0.
    d = defaultdict(int)
    for s in get_preferences():
        for c in s['ordered-preference']:
            d[c] += 1
            t += 1
        # print '   -'
        # for k, v in s.items():
        #     print k, '-', v
    print '\n$ python createstudentpref.py'
    print '\n\tRegistration averages:\n'
    for k, v in d.items():
        print k, v/t*23
    print '-'

