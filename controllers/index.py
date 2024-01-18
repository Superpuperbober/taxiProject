from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.index_model import get_passanger, get_drive_passanger,\
    get_new_passanger, borrow_drive, set_return_date, add_drive, add_org

@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()

    if request.values.get('passanger'):
        passanger_id = int(request.values.get('passanger'))
        session['passanger_id'] = passanger_id
    elif request.values.get('new_passanger'):
        new_passanger = request.values.get('new_passanger')
        session['passanger_id'] = get_new_passanger(conn, new_passanger)
    elif request.values.get('drive'):
        drive_id = int(request.values.get('drive'))
        borrow_drive(conn, drive_id, session['passanger_id'])
    elif request.values.get('return_val'):
        drive_passanger_id = request.values.get("return_val")
        set_return_date(conn, drive_passanger_id)
    elif request.values.get('add_new_drive'):
        title = request.values.get('title')
        wherego = int(request.values.get('wherego'))
        fromgo = int(request.values.get('fromgo'))
        price = int(request.values.get('price'))
        available_numbers = int(request.values.get('available_numbers'))

        drive_id = add_drive(conn, title, wherego, fromgo, price, available_numbers)
        org_id = request.values.get('org')
        add_org(conn, drive_id, org_id)

    else:
        if "passanger_id" in session.keys():
            session['passanger_id'] = session['passanger_id']
        else:
            session['passanger_id'] = 1
    df_passanger = get_passanger(conn)
    df_drive_passanger = get_drive_passanger(conn, session['passanger_id'])

    html = render_template(
        'index.html',
        passanger_id=session['passanger_id'],
        combo_box=df_passanger,
        drive_passanger=df_drive_passanger,
        len=len,
    )
    return html
