import pandas

def get_org_count(conn):
    return pandas.read_sql(
        '''
            WITH cte (org_name, org_count) AS (
                SELECT
                    org_name,
                    COUNT(drive_id)
                FROM
                    org 
                    JOIN drive_org USING (org_id)
                    JOIN drive USING (drive_id)
                GROUP BY
                    org_name
            )
            SELECT * FROM cte
        ''',
        conn
    )

def get_wherego_count(conn):
    return pandas.read_sql(
        '''
            WITH cte (wherego_name, wherego_count) AS (
                SELECT
                    wherego_name,
                    COUNT(drive_id)
                FROM
                    wherego
                    JOIN drive USING (wherego_id)
                GROUP BY
                    wherego_name
            )
            SELECT * FROM cte
        ''',
        conn
    )

def get_fromgo_count(conn):
    return pandas.read_sql(
        '''
            WITH cte (fromgo_name, fromgo_count) AS (
                SELECT
                    fromgo_name,
                    COUNT(drive_id)
                FROM
                    fromgo
                    JOIN drive USING (fromgo_id)
                GROUP BY
                    fromgo_name
            )
            SELECT * FROM cte
        ''',
        conn
    )

def get_all_orgs(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT org_name FROM org")
    orgs = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return orgs

def get_all_wheregos(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT wherego_name FROM wherego")
    wheregos = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return wheregos

def get_all_fromgos(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT fromgo_name FROM fromgo")
    fromgos = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return fromgos


def get_filtered_drives(conn, selected_orgs, selected_wheregos, selected_fromgos):
    return pandas.read_sql(
        '''
            WITH get_orgs (drive_id, orgs) AS (
                SELECT
                    drive_id,
                    GROUP_CONCAT(org_name, ", ")
                FROM
                    drive
                    JOIN drive_org USING (drive_id)
                    JOIN org USING (org_id)
                WHERE
                    org_name IN {}
                GROUP BY
                    drive_id
            ),
            get_drives AS (
                SELECT
                    title,
                    orgs,
                    wherego_name,
                    fromgo_name,
                    price,
                    available_numbers,
                    drive_id
                FROM
                    get_orgs
                    JOIN drive USING (drive_id)
                    JOIN fromgo USING (fromgo_id)
                    JOIN wherego USING (wherego_id)
                WHERE
                    fromgo_name IN {}
                    AND wherego_name IN {}
            )
            SELECT
                *
            FROM get_drives
        '''.format(
                '({})'.format(', '.join([f'"{elem}"' for elem in selected_orgs])),
                '({})'.format(', '.join([f'"{elem}"' for elem in selected_fromgos])),
                '({})'.format(', '.join([f'"{elem}"' for elem in selected_wheregos]))
            ),
        conn
    )