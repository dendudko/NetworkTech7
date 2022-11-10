import pandas as pd


def get_table(con, t_name):
    return pd.read_sql(f"SELECT * FROM {t_name};", con)


def get_table_names(con):
    table_names = pd.read_sql("SELECT name from sqlite_sequence;", con)
    table_names = table_names.name.tolist()
    return table_names
