import sys
import datetime
import os
from tools import ArgsHandler as ah

redundantArgs = ["", "\n", " "]
gitHubLink = "https://github.com/Matija-Djordjevic/sql-table-generator"

if __name__=="__main__":
    if not os.path.exists("in.txt"):
        open("in.txt", "w")
        print(f"No 'in.txt' file!\nMade you one :)\nFor help, check:\n{gitHubLink}")
        exit()

    inFile = open("in.txt", "r")

    sqlOutFile = open("create-db.sql", "w+")
    inSortedFile = open("sorted-in.txt", "w+")
    logFile  = open("log.txt", "a")

    logFile.write(f"{datetime.datetime.now()}" + "\n")

    inFileCont = inFile.read()

    if ah.strContainsInvArgs(inFileCont.lower()):
        logFile.write(f"Invalid keywords in 'in.txt' such as: {" ".join(ah.invalidArgs)}" + "\n\n")
        print("Errors occurred, check 'log.txt' for more info!")
        exit()
    
    tables = sorted(inFileCont.split("\n"))

    tables = [_ for _ in filter(lambda x: x not in redundantArgs, tables)]

    nameErrorsOccured = False
    for (ind, table) in enumerate(tables):
        tebleNameAndColumns = table.split(" ")
        tebleNameAndColumns = [_ for _ in filter(lambda x: x not in redundantArgs, tebleNameAndColumns)]
        
        tableName = tebleNameAndColumns[0]
        if not ah.isValidTableNameArg(tableName):
            nameErrorsOccured = True
            ah.displayTableNameErrs(tableName, end="\n", showMsg=True)
            logFile.write(f"    Line {ind} ('in.txt'): Fixed table name: {tableName} -> ")
            tableName = ah.fixTableNameArg(tableName)
            logFile.write(f"{tableName}\n")
        
        columns = tebleNameAndColumns[1:]

        # columns that end with _id last, rest sorted by alpha order
        columns = sorted(columns, key = lambda x : chr(sys.maxunicode) if x.endswith("_id") else x)
        
        # let us check and fix column/foreign key arguments
        for (ind, columnName) in enumerate(columns):
            isKey = ah.isForeignKeyArg(columnName)
            logFunct = ah.logForeignKeyErrsIfAny if isKey else ah.logColumnErrsIfAny
            fixedName = logFunct(columnName, logFile, ind)

            if fixedName != columnName:
                nameErrorsOccured = True
                columns[ind] = fixedName

        # section that writes SQL
        inSortedFile.write(tableName + (" " if columns != [] else ""))
        inSortedFile.write(" ".join(columns) + "\n")
        
        sqlOutFile.write(f"CREATE TABLE {tableName} (\n")
        sqlOutFile.write(f"    {tableName.lower()}_id INTEGER PRIMARY KEY AUTOINCREMENT,\n")
        sqlOutFile.write(f"    created TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,\n")
        sqlOutFile.write(f"    modified TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP")
        sqlOutFile.write("\n" if len(columns) == 0 else ",\n")
        
        areAnyArgsForeignKeys = len(list(filter(ah.isForeignKeyArg, columns))) >= 1
        
        # we do not filter out foreign keys because they need to be present as a column names as well
        for ind, columnName in enumerate(columns):
            sqlOutFile.write(f"    {columnName.lower()} INTEGER NOT NULL")
            if areAnyArgsForeignKeys or ind != len(columns) - 1:
                sqlOutFile.write(f",")

            sqlOutFile.write(f"\n")

        foreignKeys = list(filter(lambda x: x.endswith("_id"), columns))
        for ind, foreignKey in enumerate(foreignKeys):
            foreignTableName  = foreignKey[:-3]
            foreignKeyName    =  f"{tableName.lower()}_{foreignTableName.lower()}_fk"
            foreignColumnName = foreignKey.lower()
            
            sqlOutFile.write(f"    CONSTRAINT {foreignKeyName} FOREIGN KEY ({foreignColumnName}) REFERENCES {foreignTableName}({foreignColumnName})")

            if ind != len(foreignKeys) - 1:
                sqlOutFile.write(f",")

            sqlOutFile.write(f"\n")

        # end of SQL writing
        sqlOutFile.write(f");\n")
    
    logFile.write("\n") 

    if nameErrorsOccured:
        print("\nDon't worry, names are fixed!")
    
    print("Check the 'log.txt' file for more info")

    
