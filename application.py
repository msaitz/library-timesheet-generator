from flask import (Flask, flash, render_template, request,
                    url_for, send_from_directory, jsonify)
from flask_session import Session
from lib import Shift, TimeSheet, Staff, Symbol
import os
import random
import copy

#configure application
app = Flask(__name__, static_url_path='/uploads')
app.secret_key = 'super secret key'

cache = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print('post!')
        print(cache)
        return render_template('index.html', modify=True)
    
    return render_template('index.html', cbody='body id="forms"')

    
@app.route('/timesheet', methods=['GET', 'POST'])
def timesheet():
    if request.method == 'POST':
        staff_number = int(request.form['num'])
        name_list = []
        job_list = []
        start_list = []
        finish_list = []
        
        for i in range(1, staff_number + 1):
                name_list.append(request.form['name' + str(i)])
                job_list.append(request.form['job' + str(i)])
                start_list.append(request.form['start' + str(i)])
                finish_list.append(request.form['finish' + str(i)])
        
        cache['name'] = name_list
        cache['job'] = job_list
        cache['start'] = start_list
        cache['finish'] = finish_list
        cache['staff_number'] = staff_number 
        timesheet = TimeSheet(cache)
        print(cache)
         
        return render_template('result.html')
    
    else:
        return render_template('index.html')


@app.route('/timesheet/t')
def regenerate():
    if cache:
        timesheet = TimeSheet(cache)
        timesheet.create_timetable() 
    
        table = copy.deepcopy(timesheet.table)
        table.insert(0, Shift.time_slots)
        return jsonify(table=table, names=cache['name'])
    
    return render_template('index.html')


@app.route('/timesheet/gen')
def test():
    timesheet = TimeSheet(cache)
    timesheet.create_timetable()
    timesheet.print_table()
    return render_template('result.html')


@app.route('/data')
def modify_data():
    if cache:
        return jsonify(cache=cache)


app.route('/uploads/<path:filename>')
def download(filename):
    with open('uploads/test.txt', 'w') as f:
        f.write('comeme la po')
    
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)

app.run(debug=True, host='0.0.0.0')
