""" 
Module for generating SQL for creating new tables in SQLite
Documentation: https://github.com/Matija-Djordjevic/sql-table-generator
"""

import sys
import datetime
import os
from tools import ArgsHandler as ah

REDUNDANT_ARGS = ["", "\n", " "]
GITHUB_LINK = "https://github.com/Matija-Djordjevic/sql-table-generator"

def write_forign_key(foreign_key, sql_out_file):
    foreign_table_name  = foreign_key[:-3]
    foreign_key_name    = f"{table_name.lower()}_{foreign_table_name.lower()}_fk"
    foreign_column_name = foreign_key.lower()
    sql_out_file.write(f"    CONSTRAINT {foreign_key_name} FOREIGN KEY ({foreign_column_name}) REFERENCES {foreign_table_name}({foreign_column_name})")

if __name__=="__main__":
    log_file  = open("log.txt", "a", encoding="utf-8")
    log_file.write(f"{datetime.datetime.now()}\n")
    
    if not os.path.exists("in.txt"):
        open("in.txt", "w", encoding="utf-8")
        log_file.write("Aborted: 'in.txt' file missing!\n\n\n")
        print(f"No 'in.txt' file!\nMade you one :)\nFor help, check:\n{GITHUB_LINK}")
        exit()
        
    sql_out_file = open("create-db.sql", "w+", encoding="utf-8")
    sorted_in_file = open("sorted-in.txt", "w+", encoding="utf-8")
    
    in_file = open("in.txt", "r", encoding="utf-8")
    in_file_cont = in_file.read()
    in_file.close()

    if ah.contains_invalid_args(in_file_cont.lower()):
        log_file.write(f"Invalid keywords in 'in.txt' such as: {' '.join(ah.INVALID_ARGS)}" + "\n\n")
        print("Errors occurred, check 'log.txt' for more info!")
        exit()
    
    # data curration
    lines = in_file_cont.split("\n")
    
    def can_represent_table(line: str):
        return line not in REDUNDANT_ARGS
    tables = list(filter(can_represent_table, lines))

    tables = sorted(tables)

    tables = [table.split(" ") for table in tables]

    def can_represent_column(table: str):
        return table not in REDUNDANT_ARGS
    tables = [list(filter(can_represent_column, table)) for table in tables] 

    # name fixing
    fix_table     = ah.fix_table_name_arg
    fix_non_table = ah.fix_non_table_name_arg
    tables = [[fix_table(table[0], log_file, line_ind)] + [fix_non_table(non_table_arg, log_file, line_ind) for non_table_arg in table[1:]] for (line_ind, table) in enumerate(tables)]

    for (ind, table) in enumerate(tables):

        columns = table[1:]
        # columns that end with _id last, rest sorted by alpha order
        columns = sorted(columns, key = lambda x : chr(sys.maxunicode) if x.endswith("_id") else x)
        

        # section that writes SQL
        table_name = table[0]
        sorted_in_file.write(table_name + (" " if columns != [] else ""))
        sorted_in_file.write(" ".join(columns) + "\n")

        sql_out_file.write(f"CREATE TABLE {table_name} (\n")


        primary_and_composite_keys  = list(filter(ah.is_primary_or_composite_key, columns))
        should_generate_primary_key = len(primary_and_composite_keys) == 0
        if should_generate_primary_key:
            sql_out_file.write(f"    {table_name.lower()}_id INTEGER PRIMARY KEY AUTOINCREMENT,\n")

        sql_out_file.write("    created TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,\n")
        sql_out_file.write("    modified TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP")

        querry_ends = len(columns) == []
        if querry_ends:
            sql_out_file.write("\n);\n")
            continue
        
        sql_out_file.write(",\n")
    
        
        # SQL for columns
        for column_name in columns[1:]:
            sql_out_file.write(f"    {column_name.lower()} INTEGER NOT NULL,\n")
            
        if columns != []:
            sql_out_file.write(f"    {columns[-1].lower()} INTEGER NOT NULL")

        foreign_keys = list(filter(ah.is_foreign_key_arg, columns))
        querry_ends = foreign_keys == []
        if querry_ends:
            sql_out_file.write("\n);\n")
            continue

        sql_out_file.write(",\n")
        
        # SQL for foreign keys
        for foreign_key in foreign_keys[:-1]:
            write_forign_key(foreign_key, sql_out_file)
            sql_out_file.write(",\n")

        if foreign_keys != []:
            write_forign_key(foreign_keys[-1], sql_out_file)


        querry_ends = primary_and_composite_keys == []
        if querry_ends:
            sql_out_file.write("\n);\n")
            continue
        
        sql_out_file.write(",\n")

        # now lets wirte primary or composite keys if user defined any 
        if (primary_and_composite_keys != []):
            sql_out_file.write(f"    PRIMARY KEY ({', '.join(map(lambda x: x[3: ], primary_and_composite_keys))})\n")

        # now query does end
        sql_out_file.write(");\n")
    
    sql_out_file.close()

    log_file.write("\n\n")
    log_file.close()

    sorted_in_file.close()
    
    print("Done, check the 'log.txt' file for more info!")
