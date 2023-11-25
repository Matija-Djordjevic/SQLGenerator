class ArgsHandler():
    """
    Handle arguments that represent table names, column names and foreign key naems.
    Fix them, print their invalid characters or validate them.
    """
    
    INVALID_ARGS = [" created ", " modified "]

    @staticmethod
    def contains_invalid_args(args: str):
        """" Samo da mu bude malo lakse """
        for iArg in ArgsHandler.INVALID_ARGS:
            if iArg in args:
                return True
            
        return False
    
    @staticmethod
    def is_valid_table_name(table_name: str):
        return table_name[0].isupper() and "_" not in table_name

    @staticmethod
    def is_valid_foreign_key_arg(foreign_key: str):
        before_id_part = foreign_key[:-3]
        return before_id_part[0].isupper() and "_" not in before_id_part
    
    @staticmethod
    def is_valid_primary_or_composite_key(key_name: str):
        if ArgsHandler.is_foreign_key_arg(key_name):
            after_key_part = key_name[3:]
            return ArgsHandler.is_valid_foreign_key_arg(after_key_part)
        else:
            return ArgsHandler.is_valid_column_name_arg(key_name)
    
    @staticmethod
    def is_valid_column_name_arg(column_name: str):
        return column_name.islower()

    @staticmethod
    def is_foreign_key_arg(foreign_key: str):
        return foreign_key.endswith("_id") and foreign_key != "key_id"

    @staticmethod
    def is_primary_or_composite_key(key_name: str):
        return key_name != "key_id" and key_name.startswith("key") and len(key_name) > 3
    
    @staticmethod
    def fix_column_name_arg(column_name: str, log_file, err_line_ind, print_to_log = True) -> str:
        if print_to_log:
            log_file.write(f"    Line {int(err_line_ind)} ('in.txt'): Fixed COLUMN name: {column_name} -> ")
            
        fixed_name = column_name.lower()
        
        if print_to_log:
            log_file.write(f"{fixed_name}\n")

        return fixed_name

    @staticmethod
    def fix_foreign_key_arg(foreign_key_name: str, log_file, err_line_ind, print_to_log = True) -> str:
        if print_to_log:
            log_file.write(f"    Line {int(err_line_ind)} ('in.txt'): Fixed FOREIGN KEY name: {foreign_key_name} -> ")
        # TableName_id
        beofre_id = foreign_key_name[:-3]
        fixed_name = beofre_id.replace("_", "").capitalize() + "_id"
        
        if print_to_log:
            log_file.write(f"{fixed_name}\n")

        return fixed_name

    @staticmethod
    def fix_table_name_arg(table_name: str, log_file, err_line_ind) -> str:
        if not ArgsHandler.is_valid_table_name(table_name):
            log_file.write(f"    Line {int(err_line_ind)} ('in.txt'): Fixed TABLE name: {table_name} -> ")
            table_name = table_name.replace("_", "").capitalize()
            log_file.write(f"{table_name}\n")
    
        return table_name

    @staticmethod
    def fix_primary_or_composite_key(key_name: str, log_file, err_line_ind) -> str:
        log_file.write(f"    Line {int(err_line_ind)} ('in.txt'): Fixed PRIMARY/COMPOSITE KEY name: {key_name} -> ")
        if ArgsHandler.is_foreign_key_arg(key_name):
            # keyTableName_id
            fixed_name = 'key' + ArgsHandler.fix_foreign_key_arg(key_name[3 : ], log_file, err_line_ind, print_to_log = False)
        else:
            # keycolumnname_id
            fixed_name = ArgsHandler.fix_column_name_arg(key_name, log_file, err_line_ind, print_to_log = False)
            
        log_file.write(f"{fixed_name}\n")
        
        return fixed_name
    
    @staticmethod
    def fix_non_table_name_arg(arg_name: str, log_file, err_line_ind) -> str:
        if ArgsHandler.is_primary_or_composite_key(arg_name):
            if not ArgsHandler.is_valid_primary_or_composite_key(arg_name):
                return ArgsHandler.fix_primary_or_composite_key(arg_name, log_file, err_line_ind)
            
        elif ArgsHandler.is_foreign_key_arg(arg_name):
              if not ArgsHandler.is_valid_foreign_key_arg(arg_name):
                return ArgsHandler.fix_foreign_key_arg(arg_name, log_file, err_line_ind)
              
        elif not ArgsHandler.is_valid_column_name_arg(arg_name):
                return ArgsHandler.fix_column_name_arg(arg_name, log_file, err_line_ind)
        
        return arg_name
     
