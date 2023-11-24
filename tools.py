class ArgsHandler():
    class TermColors:
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'

    invalidArgs = [" created ", " modified "]

    def printValidChar(c, isInvalid = False):
        if isInvalid:
            print(f"{ArgsHandler.TermColors.FAIL}{ArgsHandler.TermColors.BOLD}{c}{ArgsHandler.TermColors.ENDC}", end="")
        else:
            print(c, end="")

    def strContainsInvArgs(str):
        for iArg in ArgsHandler.invalidArgs:
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

    def logForeignKeyErrsIfAny(keyName, logFile, lineInd=""):
        fixedName = keyName
        if not ArgsHandler.isValidForeignKeyArg(keyName):
            ArgsHandler.displayForeignKeyErrs(keyName, end="\n", showMsg=True)
            logFile.write(f"    Line {lineInd} ('in.txt'): Fixed foreign key name: {keyName} -> ")
            fixedName = ArgsHandler.fixForeignKeyArg(keyName)
            logFile.write(f"{fixedName}\n")

        return fixedName

    def logColumnErrsIfAny(columnName, logFile, lineInd=""):
        fixedName = columnName
        if not ArgsHandler.isValidColumnNameArg(columnName):
            ArgsHandler.displayColumnErrs(columnName, end="\n", showMsg=True)
            logFile.write(f"    Line {lineInd} ('in.txt'): Fixed column name: {columnName} -> ")
            fixedName = ArgsHandler.fixColumnNameArg(columnName)
            logFile.write(f"{columnName}\n")

        return fixedName

    def fixColumnNameArg(str):
        return str.lower()

    def fixForeignKeyArg(str):
        return ArgsHandler.fixTableNameArg(str[:-3]) + "_id"

    def displayTableNameErrs(str, end="", showMsg = False):
        if showMsg:
            print("Invalid table name: ", end="")

        for ind, c in enumerate(str):
            ArgsHandler.printValidChar(c, isInvalid = (c == "_" or ind == 0 and c.islower()))

        print(end=end)

    def displayForeignKeyErrs(str, end="", showMsg = False):
        if showMsg:
            print("Invalid foreign key name: ", end="")
            
        sufix = str[:-3] 
        ArgsHandler.displayTableNameErrs(sufix)

        print("_id", end=end)

    def displayColumnErrs(str, end="", showMsg = False):
        if showMsg:
            print("Invalid column name: ", end="")

        for c in str:
            ArgsHandler.printValidChar(c, isInvalid = (c.isupper()))

        print(end=end)