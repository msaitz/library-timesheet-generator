from flask import (Flask, flash, render_template, request, session,
                    url_for, send_from_directory, jsonify)
from flask_session import Session
from lib import Shift, TimeSheet, Staff, Symbol
import os
import time
import random
import copy

#configure application
app = Flask(__name__, static_url_path='/uploads')
app.secret_key = 'super secret key'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return render_template('index.html', modify=True)
    
    return render_template('index.html', cbody='body id="forms"')

    
@app.route('/timesheet', methods=['GET', 'POST'])
def timesheet():
    if request.method == 'POST':
        staff_number = int(request.form['num'])
        
        staff_info = {}
        for i in range(1, staff_number + 1):
            staff = {'name': request.form['name' + str(i)],
                    'job': request.form['job' + str(i)],
                    'start': request.form['start' + str(i)],
                    'finish': request.form['finish' + str(i)]}

            staff_info['staff' + str(i)] = staff
            staff_info['staff_number'] = staff_number
        
        session['cache'] = staff_info
        return render_template('result.html')
    else:
        return render_template('index.html')


@app.route('/timesheet/t')
def regenerate():
    if session['cache']:
        start = time.time()
        timesheet = TimeSheet(session['cache'])
        timesheet.create_timetable() 
        end = time.time() 
        calc_time = format((end - start), '.4f')
    
        table = copy.deepcopy(timesheet.table)
        table.insert(0, Shift.time_slots)
        return jsonify(table=table, names=session['cache'], time=calc_time)
    
    return render_template('index.html')


@app.route('/data')
def modify_data():
    if session['cache']:
        return jsonify(cache=session['cache'])


app.route('/uploads/<path:filename>')
def download(filename):
    with open('uploads/test.txt', 'w') as f:
        f.write('comeme la po')
    
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)

app.run(debug=True, host='0.0.0.0')
