import constants
from app import app
from flask import render_template


@app.route('/', methods=['GET'])
def index(name='', gender='', program='', subjects_select='', olympiads_select=''):
    # выводим форму
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
    return html
