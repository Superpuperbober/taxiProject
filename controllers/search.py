from app import app
from flask import render_template, request
from utils import get_db_connection
from models.search_model import get_org_count, get_wherego_count, get_fromgo_count, get_filtered_drives, get_all_orgs, get_all_wheregos, get_all_fromgos

@app.route('/search', methods=['GET', 'POST'])
def search():
    conn = get_db_connection()

    selected_orgs = []
    selected_wheregos = []
    selected_fromgos = []

    df_orgs = get_org_count(conn)
    df_wheregos = get_wherego_count(conn)
    df_fromgos = get_fromgo_count(conn)
    df_drives = get_filtered_drives(
            conn,
            get_all_orgs(conn),
            get_all_wheregos(conn),
            get_all_fromgos(conn)
        )
    
    if request.method == 'POST':
        if 'confirm' in request.form:
            selected_orgs = request.form.getlist("orgs")
            selected_wheregos = request.form.getlist("wheregos")
            selected_fromgos = request.form.getlist("fromgos")

        if 'reset' in request.form:
            selected_orgs = []
            selected_wheregos = []
            selected_fromgos = []
        
        df_drives = get_filtered_drives(
            conn,
            get_all_orgs(conn) if not selected_orgs else selected_orgs,
            get_all_wheregos(conn) if not selected_wheregos else selected_wheregos,
            get_all_fromgos(conn) if not selected_fromgos else selected_fromgos
        )

    html = render_template(
        'search.html',
        selected_orgs=selected_orgs,
        df_orgs=df_orgs,
        selected_wheregos=selected_wheregos,
        df_wheregos=df_wheregos,
        selected_fromgos=selected_fromgos,
        df_fromgos=df_fromgos,
        df_drives=df_drives
    )
    return html
