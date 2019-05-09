from flask import Blueprint, request, render_template
from pony.orm import *
import json, arrow

bp = Blueprint('schedule', __name__, url_prefix='/schedule')

@bp.route('/<type>', methods=['GET'])
@db_session
def getSchedule(type):
    params = request.args

    now = arrow.now().date()

    start_date = arrow.get(now)
    end_date = arrow.get(now).shift(days=+1)

    if 'start_date' in params.keys():
        start_date = arrow.get(params['start_date'])

    if 'end_date' in params.keys():
        end_date = arrow.get(params['end_date'])


    return json.dumps({'start': start_date.format('YYYY-MM-DD'), 'end': end_date.format('YYYY-MM-DD')})
