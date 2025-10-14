#!/usr/bin/env python3

from modules.confread import confread
from modules.database import dataman

def main():
    cnf = confread()               # Create an instance that reads our config file.
    cnf.verify_integrity()         # Make sure its at least filled in.
    conn_str = cnf.build_connstr() # Generate the connection string.

    dbc = dataman()                # Create a class instance.
    dbc.connect(conn_str)          # Connect to a database, or try to.
    dbc.verify_connection()        # Send a bogus query to test the connection.

    tables = dbc.get_tables()
    print(tables)

    for table in tables:
        columns = dbc.get_schema(table)
        print(columns)

    print("Done.")

main()