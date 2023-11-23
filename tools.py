
class TermColors:
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def printValidChar(c, isInvalid = False):
    if isInvalid:
        print(f"{TermColors.FAIL}{TermColors.BOLD}{c}{TermColors.ENDC}", end="")
    else:
        print(c, end="")

invalidArgs = [" created ", " modified "]
def strContainsInvArgs(str):
    for iArg in invalidArgs:
        if iArg in str:
            return True
        
    return False

def isValidTableNameArg(str):
    return str[0].isupper() and "_" not in str

def isValidForeignKeyArg(str):
    return str[0].isupper() and "_" not in str[:-3]

def isForeignKeyArg(str):
    return str.endswith("_id")

def isValidColumnNameArg(str):
    return str.islower()

def fixTableNameArg(str):
    return str.replace("_", "").capitalize()

def fixColumnNameArg(str):
    return str.lower()

def fixForeignKeyArg(str):
    return fixTableNameArg(str[:-3]) + "_id"

def displayTableNameErrs(str, end="", showMsg = False):
    if showMsg:
        print("Invalid table name: ", end="")

    for ind, c in enumerate(str):
        printValidChar(c, isInvalid = (c == "_" or ind == 0 and c.islower()))

    print(end=end)

def displayForeignKeyErrs(str, end="", showMsg = False):
    if showMsg:
        print("Invalid foreign key name: ", end="")
        
    sufix = str[:-3] 
    displayTableNameErrs(sufix)

    print("_id", end=end)

def displayColumnErrs(str, end="", showMsg = False):
    if showMsg:
        print("Invalid column name: ", end="")

    for c in str:
        printValidChar(c, isInvalid = (c.isupper()))

    print(end=end)