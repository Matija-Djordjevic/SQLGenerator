""" 
Module for generating SQL for creating new tables in SQLite
Documentation: https://github.com/Matija-Djordjevic/sql-table-generator
"""

import sys
import datetime
import os
from tools import ArgsHandler as ah

redundanat_args = ["", "\n", " "]
GITHUB_LINK = "https://github.com/Matija-Djordjevic/sql-table-generator"

if __name__=="__main__":
    if not os.path.exists("in.txt"):
        open("in.txt", "w", encoding="utf-8")
        print(f"No 'in.txt' file!\nMade you one :)\nFor help, check:\n{GITHUB_LINK}")
        exit()

    in_file = open("in.txt", "r", encoding="utf-8")

    sql_out_file = open("create-db.sql", "w+", encoding="utf-8")
    sorted_in_file = open("sorted-in.txt", "w+", encoding="utf-8")
    log_file  = open("log.txt", "a", encoding="utf-8")

    log_file.write(f"{datetime.datetime.now()}" + "\n")

    in_file_cont = in_file.read()

    if ah.contains_invalid_args(in_file_cont.lower()):
        log_file.write(f"Invalid keywords in 'in.txt' such as: {" ".join(ah.invalidArgs)}" + "\n\n")
        print("Errors occurred, check 'log.txt' for more info!")
        exit()
    
    tables = sorted(in_file_cont.split("\n"))

    tables = [_ for _ in filter(lambda x: x not in redundanat_args, tables)]

    naming_errs_occured = False
    for (ind, table) in enumerate(tables):
        table_name_and_columns = table.split(" ")
        table_name_and_columns = [_ for _ in filter(lambda x: x not in redundanat_args, table_name_and_columns)]
        
        table_name = table_name_and_columns[0]
        if not ah.is_valid_table_name(table_name):
            naming_errs_occured = True
            ah.display_table_name_errs(table_name, end="\n", show_msg=True)
            log_file.write(f"    Line {ind} ('in.txt'): Fixed table name: {table_name} -> ")
            table_name = ah.fix_table_name_arg(table_name)
            log_file.write(f"{table_name}\n")
        
        columns = table_name_and_columns[1:]

        # columns that end with _id last, rest sorted by alpha order
        columns = sorted(columns, key = lambda x : chr(sys.maxunicode) if x.endswith("_id") else x)
        
        # let us check and fix column/foreign key arguments
        for (ind, column_name) in enumerate(columns):
            IS_KEY = ah.is_foreign_key_arg(column_name)
            LOG_FUNCT = ah.log_foreign_key_errs_if_any if IS_KEY else ah.log_column_errs_if_any
            
            FIXED_NAME = LOG_FUNCT(column_name, log_file, ind)

            if FIXED_NAME != column_name:
                naming_errs_occured = True
                columns[ind] = FIXED_NAME

        # section that writes SQL
        sorted_in_file.write(table_name + (" " if columns != [] else ""))
        sorted_in_file.write(" ".join(columns) + "\n")
        
        sql_out_file.write(f"CREATE TABLE {table_name} (\n")
        sql_out_file.write(f"    {table_name.lower()}_id INTEGER PRIMARY KEY AUTOINCREMENT,\n")
        sql_out_file.write("    created TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,\n")
        sql_out_file.write("    modified TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP")
        sql_out_file.write("\n" if len(columns) == 0 else ",\n")
        
        are_any_args_foreign = len(list(filter(ah.is_foreign_key_arg, columns))) >= 1
        
        # we do not filter out foreign keys because they need to be present as a column names as well
        for ind, column_name in enumerate(columns):
            sql_out_file.write(f"    {column_name.lower()} INTEGER NOT NULL")
            if are_any_args_foreign or ind != len(columns) - 1:
                sql_out_file.write(",")

            sql_out_file.write("\n")

        foreign_keys = list(filter(lambda x: x.endswith("_id"), columns))
        for ind, foreign_key in enumerate(foreign_keys):
            foreign_table_name  = foreign_key[:-3]
            foreign_key_name    = f"{table_name.lower()}_{foreign_table_name.lower()}_fk"
            foreign_column_name = foreign_key.lower()
            
            sql_out_file.write(f"    CONSTRAINT {foreign_key_name} FOREIGN KEY ({foreign_column_name}) REFERENCES {foreign_table_name}({foreign_column_name})")

            if ind != len(foreign_keys) - 1:
                sql_out_file.write(",")

            sql_out_file.write("\n")

        # end of SQL writing
        sql_out_file.write(");\n")
    
    log_file.write("\n") 

    if naming_errs_occured:
        print("\nDon't worry, names are fixed!")
    
    print("Check the 'log.txt' file for more info")
