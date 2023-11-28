# Generate SQL for creating SQLite tables
### How to run:
1. Clone this repo.
2. Navigate to the root folder and in it, create the `in.txt` file. 
3. Fill in the `in.txt` file while followingn the [rules for naming arguments](#arguments-naming).<br>
	Example:
	> TableName1 column_name1 colum_name2 keyTableName3_id <br>
	> TableName2 <br>
	> TableName3 column_name1 TableName1_id column_name2 <br>
	> TableName4 keykey_name1 <br>
4. Run `main.py`.<br>

### After running:
The `main.py` script will create `sorted-in.txt`, `create-db.sql` and `log.txt` file in the root folder.<br>
Navigate to the `create-db.sql` file to view the newly generated SQL. <br>
Additionally, you can now check the `sorted-in.txt` file. It contains the sorted contents of the `in.txt` file.

### Arguments naming
>  
> * `table name` arguments: <br>
Every line must start with one and contain only one. These arguments must be capitalized and can contain small and capital letters, as well as digits. <br><br> 
> * `column` arguments: <br> 
They can contain small letters, digits and `'_'` symbols. They represent the column name of the table, and will be assigned an INTEGER data type in the table. <br><br> 
> * `foreign key` arguments: <br>
These arguments must end with a `"_id"` suffix. The part before the `"_id"` should reference an existing table, and follow the naiming rules for `table name` arguments.<br><br> 
> * `primary/foreign key` arguments: <br>
A `primary/foreign key` argument must start with a `"key"` prefix. <br>

### Note Before Using
>  * If `table name` argument isn't capitalized, the script will do it
> automatically. Also, it will remove any `'_'` characters from it as well.<br>
>  * If `column` argument contains any capital letters, running the script
> will replace them with their lower case counterparts. <br>
>  * Part of the `foreign key` argument before the `"_id"` will be treated as if it was a `table name` argument. <br>
> * If `primary/foreign key` argument represents a column name, the part followinf a `"key"` prefix will be treated as if it was a `column` argument. 
And if it represents a foreign key, it's post `"key"` part would be treated as if it was a
`foreign key` argument. 
>
> These changes will be present in both the `create-db.sql` file and the `sorted-in.txt` file.<br>
> Check the `log.txt` file for the verbose explanations on these and other user mistakes, and for the script failures.
<br>
