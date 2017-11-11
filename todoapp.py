#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""to do app"""


import re
import pickle
from flask import Flask, render_template, request, redirect


TO_DO_LIST = []

try:
    with open('my_list.pickle', 'rb') as import_list:
        IMPORT_ITEMS = pickle.load(import_list)
    for item in IMPORT_ITEMS:
        TO_DO_LIST.append(item)
except IOError:
    pass

app = Flask(__name__)

@app.route('/')
def main_page():
    """brings up the main web page"""
    return render_template('index.html', TO_DO_LIST=TO_DO_LIST)

@app.route('/submit', methods=['POST'])
def submit_task():
    """adds a task to the to do list"""
    new_task = request.form['task'].strip()
    new_task_email = request.form['email'].strip()
    new_priority = request.form['priority']
    if new_task:
        if re.match(r'[^@]+@[^@]+\.[^@]+', new_task_email):
            add_to_list = [new_task, new_task_email, new_priority]
            TO_DO_LIST.append(add_to_list)
            return redirect('/')
        else:
            return redirect('/')

@app.route('/clear', methods=['POST'])
def clear_list():
    """clears the to do list"""
    while TO_DO_LIST:
        TO_DO_LIST.pop()
        with open('my_list.pickle', 'wb') as my_list:
            pickle.dump(TO_DO_LIST, my_list, protocol=pickle.HIGHEST_PROTOCOL)
    return redirect('/')

@app.route('/save', methods=['POST'])
def save_list():
    """saves the to do list to a pickle file"""
    with open('my_list.pickle', 'wb') as my_list:
        pickle.dump(TO_DO_LIST, my_list, protocol=pickle.HIGHEST_PROTOCOL)
    return redirect('/')


if __name__ == '__main__':
    app.run()
