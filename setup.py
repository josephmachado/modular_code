import os
import duckdb


def clean_up(file):
    # Remove the file if it exists
    if os.path.exists(file):
        os.remove(file)
    else:
        print(f"The file {file} does not exist.")


def create_input_data(db_name: str = 'database.db', setup_script: str = './create_tables.sql'):
    con = duckdb.connect(
        db_name
    )  # Define a .db file to persist the generated tpch data

    with open(setup_script, 'r') as f:
        sql_script = f.read()
        
    con.sql(sql_script)  # generate a 100MB TPCH dataset
    con.commit()
    con.close()  # close connection, since duckdb only allows one connection to tpch.db


if __name__ == "__main__":
    print("Cleaning up existing DB files")
    clean_up("database.db")
    print("Creating input data")
    create_input_data()
