import pandas

def get_passanger(conn):
    return pandas.read_sql(
    '''
        SELECT * FROM passanger
    ''', 
    conn
    )

def add_org(conn, drive_id, org_id):
    cur = conn.cursor()
    cur.execute(
        f'''
                INSERT INTO drive_org (drive_id, org_id)
                VALUES
                    ({drive_id}, {org_id})
            '''
    )
    conn.commit()
    cur.close()

def add_drive(conn, title, wherego, fromgo, price, available_numbers):
    cur = conn.cursor()
    cur.execute(
        f'''
            INSERT INTO drive (title, wherego_id, fromgo_id, price, available_numbers)
            VALUES
                ('{title}', {wherego}, {fromgo}, {price}, {available_numbers})
        '''
    )
    conn.commit()
    return cur.lastrowid

def get_drive_passanger(conn, passanger_id):
    return pandas.read_sql('''
        WITH get_orgs(drive_id, orgs_name)
        AS (
            SELECT drive_id, org_name
            FROM org JOIN drive_org USING(org_id)
            GROUP BY drive_id
        )
        SELECT 
            fromgo_name AS Место_встречи,
            orgs_name AS огранизаторы,
            borrow_date AS Дата_создания, 
            return_date AS Дата_,
            drive_passanger_id
        FROM
        passanger
        JOIN drive_passanger USING(passanger_id)
        JOIN drive USING(drive_id)
        JOIN get_orgs USING(drive_id)
        join fromgo using (fromgo_id)
        WHERE passanger.passanger_id = :id
        ORDER BY 3
    ''', 
    conn, 
    params={"id": passanger_id}
    )

def get_new_passanger(conn, new_passanger):
    cur = conn.cursor()
    cur.execute(
        '''
            INSERT INTO passanger (passanger_name)
            VALUES (:new_passanger)
        ''',
        {"new_passanger": new_passanger}
    )
    conn.commit()
    return cur.lastrowid

def borrow_drive(conn, drive_id, passanger_id):
    cur = conn.cursor()
    cur.executescript(
        f'''
            INSERT INTO drive_passanger (drive_id, passanger_id, borrow_date, return_date)
            VALUES ({drive_id}, {passanger_id}, DATE("NOW"), NULL);

            UPDATE drive
            SET available_numbers = available_numbers - 1
            WHERE drive_id = {drive_id}
        ''',
    )
    conn.commit()

def set_return_date(conn, drive_passanger_id):
    cur = conn.cursor()
    cur.execute(
        f'''
            UPDATE drive_passanger
            SET return_date = DATE('NOW')
            WHERE drive_passanger_id = {drive_passanger_id}
        '''
    )
    cur.execute(
        f'''
            UPDATE drive
            SET available_numbers = available_numbers + 1
            WHERE drive_id = (SELECT drive_id FROM drive_passanger WHERE drive_passanger_id = {drive_passanger_id})
        '''
    )
    conn.commit()