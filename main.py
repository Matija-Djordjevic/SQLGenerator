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

def fixName(str):
    return str.replace("_", "").capitalize()

def isValidColName(str):
    return str.islower()

def fixColName(str):
    return str.lower()

def displayNameErrs(str):
    print(f"Bad table name:   ", end="")
    for ind, c in enumerate(str):
        if(c == "_" or ind == 0 and c.islower()):
            print(f"{bcolors.FAIL}{c}{bcolors.ENDC}", end="")
        else:
            print(f"{c}", end="")

    print()

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
        
        name    = tebleNameAndColumns[0]
        if not isValidName(name):
            errorsOccurred = True
            displayNameErrs(name)
            logFile.write(f"    Line {ind} ('in.txt'): Fixed table name: {name} -> ")
            name = fixName(name)
            logFile.write(f"{name}\n")
        
        columns = tebleNameAndColumns[1:]
        # columns that end with _id last, rest sorted by alpha order
        columns = sorted(columns, key = lambda x : chr(sys.maxunicode) if x.endswith("_id") else x)

        for (ind, column) in enumerate(columns):
            if not isValidColName(column):
                errorsOccurred = True
                displayColNameErrs(column)
                logFile.write(f"    Line {ind} ('in.txt'): Fixed column name: {column} -> ")
                columns[ind] = fixColName(column)
                logFile.write(f"{column}\n")
        
        inSortedFile.write(name + (" " if columns != [] else ""))
        inSortedFile.write(" ".join(columns) + "\n")
        
        sqlOutFile.write(f"CREATE TABLE {name} (\n")
        sqlOutFile.write(f"    {name.lower()}_id PRIMARY KEY UNIQUE,\n")
        sqlOutFile.write(f"    created TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,\n")
        sqlOutFile.write(f"    modified TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP")

        sqlOutFile.write("\n" if len(columns) == 0 else ",\n")
        
        for ind, column in enumerate(columns):
            sqlOutFile.write(f"    {column} INTEGER NOT NULL")
            sqlOutFile.write(",\n" if ind != len(columns) - 1 else "\n")

        sqlOutFile.write(f");\n")
        
    logFile.write("\n") 

    
    if errorsOccurred:
        print("Errors occurred, check 'log.txt' for more info!")
    
    
