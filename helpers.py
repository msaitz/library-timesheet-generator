#############################################
#                                           #
#   Helper functions for applyication.py    #
#                                           #
#############################################

from flask import request, Flask
from lib import Staff


def get_form_data(num):
    tmp_data = []
    staff_obj = Staff
    
    for i in range(1, num + 1):
        job = request.form['job' + str(i)]
        name = request.form['name' + str(i)]
        if not name: 
            name = 'No name'
    
        staff = {'name': name,
                'job': job,
                'start': request.form['start' + str(i)],
                'finish': request.form['finish' + str(i)],
                'sort_value': staff_obj.switcher[job]}
        tmp_data.append(staff)
    
    return tmp_data


def sort_form_data(tmp_data):
    sorted_data = sorted(tmp_data, reverse=True,
                        key=lambda k: k['sort_value'])
    formatted_data = {}
    
    for i in range(len(sorted_data)):
        formatted_data['staff' + str(i + 1)] = sorted_data[i]
    formatted_data['staff_number'] = len(sorted_data)

    return formatted_data
