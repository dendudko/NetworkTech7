import constants
from app import app
from flask import render_template, request
from controllers import index


@app.route('/hello', methods=['GET'])
def hello():
    # для каждого передаваемого параметра формы нужно задать
    # значение по умолчание, на случай если пользователь ничего не введет
    name = ""
    gender = ""
    program_id = 0
    # список из номеров выбранных пользователем дисциплин
    subject_id = []
    # список из выбранных пользователем дисциплин
    subjects_select = []
    name = request.values.get('username')
    gender = request.values.get('gender')
    program_id = request.values.get('program')
    subject_id = request.values.getlist('subject[]')
    # формируем список из выбранных пользователем дисциплин
    subjects_select = [constants.subjects[int(i)] for i in subject_id]
    # формируем список из выбранных пользователем олимпиад
    olympiad_id = request.values.getlist('olympiad[]')
    olympiads_select = [constants.olympiads[int(i)] for i in olympiad_id]
    program = constants.programs[int(program_id)]

    html = index.index(name=name, gender=gender, program=program,
                       subjects_select=subjects_select, olympiads_select=olympiads_select)
    html += render_template(
        'hello.html',
        name=name,
        gender=gender,
        program=program,
        program_list=constants.programs,
        len=len,
        subjects_select=subjects_select,
        subject_list=constants.subjects,
        olympiad_list=constants.olympiads,
        olympiads_select=olympiads_select
    )
    return html
