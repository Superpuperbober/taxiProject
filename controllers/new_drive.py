from app import app
from flask import render_template
from utils import get_db_connection
from models.new_drive_model import get_whergo, get_fromgo, get_org

@app.route('/drive', methods=['GET'])
def new_drive():
    conn = get_db_connection()

    df_wherego = get_whergo(conn)
    df_fromgo = get_fromgo(conn)
    df_org = get_org(conn)

    html = render_template(
        'new_drive.html',
        df_wherego=df_wherego,
        df_fromgo=df_fromgo,
        df_org=df_org,
        len=len,
    )
    return html
