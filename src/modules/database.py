import psycopg as pg

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