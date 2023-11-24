class ArgsHandler():
    """
    Handle arguments that represent table names, column names and foreign key naems.
    Fix them, print their invalid characters or validate them.
    """
    class TermColors:
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'

    invalidArgs = [" created ", " modified "]

    @staticmethod
    def print_char(c, is_invalid = False):
        if is_invalid:
            print(f"{ArgsHandler.TermColors.FAIL}{ArgsHandler.TermColors.BOLD}{c}{ArgsHandler.TermColors.ENDC}", end="")
        else:
            print(c, end="")

    @staticmethod
    def contains_invalid_args(args: str):
        """" Samo da mu bude malo lakse """
        for iArg in ArgsHandler.invalidArgs:
            if iArg in args:
                return True
            
        return False
    
    @staticmethod
    def is_valid_table_name(table_name: str):
        return table_name[0].isupper() and "_" not in table_name

    @staticmethod
    def is_valid_foreign_key_arg(foreign_key: str):
        return foreign_key[0].isupper() and "_" not in foreign_key[:-3]

    @staticmethod
    def is_foreign_key_arg(foreign_key: str):
        return foreign_key.endswith("_id")

    @staticmethod
    def is_valid_column_name_arg(column_name: str):
        return column_name.islower()

    @staticmethod
    def log_foreign_key_errs_if_any(key_name: str, log_file, line_ind= 0) -> str:
        fixed_name = key_name
        if not ArgsHandler.is_valid_foreign_key_arg(key_name):
            ArgsHandler.display_foreign_key_errs(key_name, end="\n", show_msg=True)
            log_file.write(f"    Line {int(line_ind)} ('in.txt'): Fixed foreign key name: {key_name} -> ")
            fixed_name = ArgsHandler.fix_foreign_key_arg(key_name)
            log_file.write(f"{fixed_name}\n")

        return fixed_name

    @staticmethod
    def log_column_errs_if_any(column_name: str, log_file, line_ind= 0) -> str:
        fixedName = column_name
        if not ArgsHandler.is_valid_column_name_arg(column_name):
            ArgsHandler.display_column_errs(column_name, end="\n", show_msg=True)
            log_file.write(f"    Line {int(line_ind)} ('in.txt'): Fixed column name: {column_name} -> ")
            fixedName = ArgsHandler.fix_column_name_arg(column_name)
            log_file.write(f"{column_name}\n")

        return fixedName

    @staticmethod
    def fix_column_name_arg(column_name: str) -> str:
        return column_name.lower()

    @staticmethod
    def fix_foreign_key_arg(foreign_key: str) -> str:
        return ArgsHandler.fix_table_name_arg(foreign_key[:-3]) + "_id"

    @staticmethod
    def fix_table_name_arg(table_name: str) -> str:
        return table_name.replace("_", "").capitalize()
    
    @staticmethod
    def display_table_name_errs(table_name: str, end="", show_msg = False):
        if show_msg:
            print("Invalid table name: ", end="")

        for ind, c in enumerate(table_name):
            ArgsHandler.print_char(c, is_invalid= (c == "_" or ind == 0 and c.islower()))

        print(end=end)

    @staticmethod
    def display_foreign_key_errs(foreign_key: str, end="", show_msg = False):
        if show_msg:
            print("Invalid foreign key name: ", end="")
            
        sufix = foreign_key[:-3] 
        ArgsHandler.display_table_name_errs(sufix)

        print("_id", end=end)

    @staticmethod
    def display_column_errs(column_name, end="", show_msg = False):
        if show_msg:
            print("Invalid column name: ", end="")

        for c in column_name:
            ArgsHandler.print_char(c, is_invalid= (c.isupper()))

        print(end=end)