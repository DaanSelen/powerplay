#!/usr/bin/env python3

import psycopg as pg
import datetime as dt
from psycopg import sql

import json

dt_format = "%Y-%m-%d %H:%M:%S.%f"

class dataman():
    def __init__(self) -> None:
        self.dbc: pg.Connection

    def connect(self, conn_str: str):
        try:
            self.dbc = pg.connect(conn_str)
            print("Connection established successfully.")

        except Exception as e:
            print("Connection failed:", e)

    def verify_connection(self):
        if not self.dbc:
            print("Not connected to any database.")
            return False
        try:
            with self.dbc.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
            print("Database connection is alive.")
            return True
        except Exception as e:
            print("Database ping failed:", e)
            return False

    def get_tables(self) -> list[str]:
        with self.dbc.cursor() as cur:
            cur.execute("""
                SELECT table_schema, table_name
                FROM information_schema.tables
                WHERE table_type = 'BASE TABLE'
                AND table_schema NOT IN ('pg_catalog', 'information_schema');
            """)
            tables = cur.fetchall()

        available_tables = []
        for _, table in tables:
            available_tables.append(table)
        return available_tables

    def get_schema(self, table_name: str, schema: str = "public"):
        query = """
            SELECT
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_schema = %s
            AND table_name = %s
            ORDER BY ordinal_position;
        """

        with self.dbc.cursor() as cur:
            cur.execute(query, (schema, table_name))
            columns = cur.fetchall()
        return columns

    def get_all_rows(self, table_name):
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
    
        with self.dbc.cursor() as cur:
            cur.execute(query)
            raw_rows = cur.fetchall()

        for ind_raw_row in raw_rows:
            print(ind_raw_row)

    def get_dist_nodeids(self, table_name):
        query = sql.SQL("SELECT DISTINCT nodeid FROM {}").format(sql.Identifier(table_name))

        with self.dbc.cursor() as cur:
            cur.execute(query)
            raw_rows = cur.fetchall()
        
        cleaned_rows = []
        for ind_raw_row in raw_rows:
            strp_row = ind_raw_row[0].strip()

            if "*" in strp_row: # Catch this nodeid, because its bogus.
                continue
            cleaned_rows.append(strp_row)
            
        return cleaned_rows

    def get_pwr_events(self, table_name, nodeid) -> list[dt.datetime, dict]:
        query = f"""
            SELECT time, doc FROM {table_name} WHERE nodeid = %s
        """
        
        with self.dbc.cursor() as cur:
            cur.execute(query, (nodeid,))
            raw_rows = cur.fetchall()
        
        return raw_rows