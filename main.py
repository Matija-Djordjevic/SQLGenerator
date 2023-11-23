from re import L
import sys
import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def isValidEntry(str):
    invs = ["", "\n", " "]
    return str not in invs

def isValidName(str):
    return str[0].isupper() and "_" not in str

def isValidIDName(str):
    return str[0].isupper() and "_" not in str[:-3]


def isValidColName(str):
    return str.islower()

def fixName(str):
    return str.replace("_", "").capitalize()

def fixColName(str):
    return str.lower()

def fixIDName(str):
    return fixName(str[:-3]) + "_id"


def displayNameErrs(str, endLn = True):
    for ind, c in enumerate(str):
        if(c == "_" or ind == 0 and c.islower()):
            print(f"{bcolors.FAIL}{c}{bcolors.ENDC}", end="")
        else:
            print(f"{c}", end="")

    if endLn: 
        print()

def displayIDNameErrs(str):
    displayNameErrs(str[:-3], endLn = False)
    print("_id")

invEntries = ["created", "modified"]
def hasInvealidEntries(str):
    for inv in invEntries:
        if inv in str:
            return True

    return False

def displayColNameErrs(str):
    print(f"Bad column name:  ", end="")
    for ind, c in enumerate(str):
        if(c.isupper()):
            print(f"{bcolors.FAIL}{c}{bcolors.ENDC}", end="")
        else:
            print(f"{c}", end="")

    print()


if __name__=="__main__":
    inFile  = open("in.txt", "r+")

        

    sqlOutFile = open("create-db.sql", "w+")
    inSortedFile = open("sorted-in.txt", "w+")
    logFile  = open("log.txt", "a")

    logFile.write(f"{datetime.datetime.now()}" + "\n")

    inFileCont = inFile.read()

    if hasInvealidEntries(inFileCont.lower()):
        logFile.write(f"Invalid keywords in 'in.txt' such as: {" ".join(invEntries)}" + "\n")
        print("Errors occurred, check 'log.txt' for more info!")
        exit()

    tables = sorted(inFileCont.split("\n"))

    tables = [_ for _ in filter(isValidEntry, tables)]

    errorsOccurred = False
    for (ind, tableStr) in enumerate(tables):
        tebleNameAndColumns = tableStr.split(" ")
        tebleNameAndColumns = [_ for _ in filter(isValidEntry, tebleNameAndColumns)]
        
        currTableName    = tebleNameAndColumns[0]
        if not isValidName(currTableName):
            errorsOccurred = True
            displayNameErrs(currTableName)
            logFile.write(f"    Line {ind} ('in.txt'): Fixed table name: {currTableName} -> ")
            currTableName = fixName(currTableName)
            logFile.write(f"{currTableName}\n")
        
        columns = tebleNameAndColumns[1:]
        # columns that end with _id last, rest sorted by alpha order
        columns = sorted(columns, key = lambda x : chr(sys.maxunicode) if x.endswith("_id") else x)

        for (ind, column) in enumerate(columns):

            if column.endswith("_id"):
                if not isValidIDName(column):
                    errorsOccurred = True
                    displayIDNameErrs(column)
                    logFile.write(f"    Line {ind} ('in.txt'): Fixed ID name: {column} -> ")
                    columns[ind] = fixIDName(column)
                    logFile.write(f"{column}\n")
            elif not isValidColName(column):
                errorsOccurred = True
                displayColNameErrs(column)
                logFile.write(f"    Line {ind} ('in.txt'): Fixed column name: {column} -> ")
                columns[ind] = fixColName(column)
                logFile.write(f"{column}\n")


        inSortedFile.write(currTableName + (" " if columns != [] else ""))
        inSortedFile.write(" ".join(columns) + "\n")
        
        sqlOutFile.write(f"CREATE TABLE {currTableName} (\n")
        sqlOutFile.write(f"    {currTableName.lower()}_id INTEGER PRIMARY KEY AUTOINCREMENT,\n")
        sqlOutFile.write(f"    created TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,\n")
        sqlOutFile.write(f"    modified TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP")

        sqlOutFile.write("\n" if len(columns) == 0 else ",\n")
        
        has_id_column = len(list(filter(lambda x: x.endswith("_id"), columns))) >= 1
        
        for ind, column in enumerate(columns):
            sqlOutFile.write(f"    {column.lower()} INTEGER NOT NULL")
            if has_id_column or ind != len(columns) - 1:
                sqlOutFile.write(f",")

            sqlOutFile.write(f"\n")


        columnsWithIdSufx = list(filter(lambda x: x.endswith("_id"), columns))
        for ind, column in enumerate(columnsWithIdSufx):
            foreignTableName  = column[:-3]
            foreignKeyName    =  f"{currTableName.lower()}_{foreignTableName.lower()}_fk"
            foreignColumnName = column.lower()
            
            sqlOutFile.write(f"    CONSTRAINT {foreignKeyName} FOREIGN KEY ({foreignColumnName}) REFERENCES {foreignTableName}({foreignColumnName})")

            if ind != len(columnsWithIdSufx) - 1:
                sqlOutFile.write(f",")

            sqlOutFile.write(f"\n")

        sqlOutFile.write(f");\n")
        
    logFile.write("\n") 

    
    if errorsOccurred:
        print("Errors occurred, check 'log.txt' for more info!")
    
    
