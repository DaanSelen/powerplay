#!/usr/bin/env python3

from modules.confread import confread
from modules.database import dataman
from modules.dataproc import process

from json import dumps

rel_table = "power"
data_table = "main"

def main():
    cnf = confread()               # Create an instance that reads our config file.
    if not cnf.verify_integrity():    # Make sure its at least filled in.
        return
    conn_str = cnf.build_connstr() # Generate the connection string.

    dbc = dataman()                # Create a class instance.
    dbc.connect(conn_str)          # Connect to a database, or try to.
    dbc.verify_connection()        # Send a bogus query to test the connection.

    dist_nodeids = dbc.get_dist_nodeids(rel_table)
    ref_data = dbc.get_doc_data(data_table)

    node_dfs = {}
    for nodeid in dist_nodeids:
        for ref in ref_data:
            if ref['nodeid'] == nodeid:
                rel_name = ref['nodename']

        print("-" * 10, f"PROCESSING: {rel_name}", "-" * 10)
        nid_rows = dbc.get_pwr_events(rel_table, nodeid)

        dataframe = process.convert(nid_rows)
        dataframe = process.insert_name(dataframe, rel_name)
        node_dfs[nodeid] = dataframe

        print(dataframe)

    print("Displaying data.")
    process.stitch_plot(node_dfs)

main()