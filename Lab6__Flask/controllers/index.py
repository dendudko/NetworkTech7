import constants
from app import app
from flask import render_template, request


@app.route('/', methods=['GET'])
def index():
    name = request.values.get('username')
    gender = request.values.get('gender')
    program_id = request.values.get('program')
    subject_id = request.values.getlist('subject[]')
    # формируем список из выбранных пользователем дисциплин
    subjects_select = [constants.subjects[int(i)] for i in subject_id]
    # формируем список из выбранных пользователем олимпиад
    olympiad_id = request.values.getlist('olympiad[]')
    olympiads_select = [constants.olympiads[int(i)] for i in olympiad_id]
    if program_id:
        program = constants.programs[int(program_id)]
    else:
        program = constants.programs[0]

    html = render_template(
        'index.html',
        program_list=constants.programs,
        subject_list=constants.subjects,
        olympiad_list=constants.olympiads,
        len=len,
        name=name,
        gender=gender,
        program=program,
        subjects_select=subjects_select,
        olympiads_select=olympiads_select
    )
    html += render_template(
        'hello.html',
        program_list=constants.programs,
        subject_list=constants.subjects,
        olympiad_list=constants.olympiads,
        len=len,
        name=name,
        gender=gender,
        program=program,
        subjects_select=subjects_select,
        olympiads_select=olympiads_select
    )
    return html
