from flask import (Flask, flash, render_template, request, session,
                    url_for, send_from_directory, jsonify)
from flask_session import Session
from lib import Shift, TimeSheet, Staff, Symbol
from helpers import *
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
        unsorted_data = get_form_data(staff_number) 
        formatted_data = sort_form_data(unsorted_data)
        session['cache'] = formatted_data

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
