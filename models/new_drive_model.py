import pandas as pd

def get_whergo(conn):
    return pd.read_sql(
    '''
            SELECT
                wherego_id,
                wherego_name
            FROM
                wherego
        ''',
        conn
    )

def get_fromgo(conn):
    return pd.read_sql(
    '''
            SELECT
                fromgo_id,
                fromgo_name
            FROM
                fromgo
        ''',
        conn
    )

def get_org(conn):
    return pd.read_sql(
        '''
                SELECT
                    org_id,
                    org_name
                FROM
                    org
            ''',
        conn
    )
