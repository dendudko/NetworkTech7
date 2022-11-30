import constants
from app import app
from flask import render_template, request


@app.route('/olympiad/<oly>')
def olympiad(oly):
    html = render_template(
        'olympiad.html',
        oly=oly,
        description=constants.olympiad_dict[oly]
    )
    return html
