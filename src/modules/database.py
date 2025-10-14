import psycopg as pg

class dataman():
    @staticmethod
    def connect(conn_str: str):
        dbc = pg.connect(conn_str)