from flask import (Flask, flash, render_template, request,
                    url_for, send_from_directory)
from flask_session import Session
from lib import Shift, TimeSheet, Staff, Symbol
import os
import random

#configure application
app = Flask(__name__, static_url_path='/uploads')
app.secret_key = 'super secret key'

cache = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        staff_number = int(request.form['num'])
        cache['staff_number'] = staff_number

        return render_template('form.html', staff_number=staff_number)
    
    else:
        return render_template('index.html')


@app.route('/timesheet', methods=['GET', 'POST'])
def timesheet():
    if request.method == 'POST':
        name_list = []
        job_list = []
        start_list = []
        finish_list = []
        
        for i in range(1, cache['staff_number'] + 1):
                name_list.append(request.form['name' + str(i)])
                job_list.append(request.form['job' + str(i)])
                start_list.append(request.form['start' + str(i)])
                finish_list.append(request.form['finish' + str(i)])
        
        cache['name'] = name_list
        cache['job'] = job_list
        cache['start'] = start_list
        cache['finish'] = finish_list

        timesheet = TimeSheet(cache)
        
        return render_template('result.html',
                                time_slots=Shift.time_slots,
                                table=timesheet.table,
                                staff_list=timesheet.staff_list,
                                list_len=len(timesheet.staff_list))
    else:
        return render_template('index.html')


@app.route('/timesheet/gen', methods=['GET', 'POST'])
def regenerate():
    if request.method == 'POST':
        timesheet = TimeSheet(cache)

        return render_template('result.html',
                                time_slots=Shift.time_slots,
                                table=timesheet.table,
                                staff_list=timesheet.staff_list,
                                list_len=len(timesheet.staff_list))
    else:
        return render_template('index.html')

@app.route('/uploads/<path:filename>')
def download(filename):
    with open('uploads/test.txt', 'w') as f:
        f.write('comeme la po')
    
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)

app.run(debug=True, host='0.0.0.0')