#!/usr/bin/python

import os
import random 
from lib import Staff
from lib import TimeSheet
from lib import Shift
 
# initialize list for storing staff members
staff_list = list()

# initialize staff objects
staff_list.append(Staff('Ozeu', Shift.staff_jobs.DLM.name))
staff_list.append(Staff('Miguel', Shift.staff_jobs.SUP.name, 14))
staff_list.append(Staff('Antonio', Shift.staff_jobs.SUP.name))
staff_list.append(Staff('Xavi', Shift.staff_jobs.LA.name, 14))
staff_list.append(Staff('Serdo', Shift.staff_jobs.LA.name))
staff_list.append(Staff('Loue', Shift.staff_jobs.LA.name, 14))
staff_list.append(Staff('Jose', Shift.staff_jobs.LA.name))
#staff_list.append(Staff('Karles', Shift.staff_jobs.LA.name))

timesheet = TimeSheet(staff_list, Shift.time_slots)
timesheet.add_shifts(staff_list, len(Shift.time_slots))

break_list = ['lunch', 'late', 'morning', 'afternoon']
for break_time in break_list:
    timesheet.break_manager(break_time, staff_list)

jobs = ['A', 'A', 'Q', 'J']
random.shuffle(jobs)
print(jobs)

for job in jobs:
    timesheet.job_manager(job, staff_list)
'''
timesheet.job_manager('A', staff_list)
timesheet.job_manager('B', staff_list)
timesheet.job_manager('C', staff_list)
timesheet.job_manager('D', staff_list)
'''

# final print of the timetable
Shift.print_time_slots()
timesheet.print_table(staff_list)

file = open('uploads/test.txt', 'w')
file.write('Test, test, test')
file.close()
