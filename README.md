# Generate SQL for creating SQLite tables

### How to run:
1. Clone this repo.
2. Navigate to the root folder and in it, create the `in.txt` file. 
3. Fill in the `in.txt` file. One line represents one table. <br>
	Example:
	> TableName1 column_name1 colum_name2 <br>
	> TableName2 <br>
	> TableName3 column_name1 TableName1_id column_name2 
4. Run `main.py`.

### After running:
The `main.py` script will create `sorted-in.txt`, `create-db.sql` and `log.txt` file in the root folder.<br>
Navigate to the `create-db.sql` file to view the newly generated SQL. <br>
Additionally, you can now check the `sorted-in.txt` file. It contains the sorted contents of the `in.txt` file.

### Schema for `in.txt`
Xs
> sdadasdasd
> sadadas

> * `"Table1Name"` is a `table name argument`. Every line must start with one and contain only one. These arguments must be capitalized and can contain small and capital letters, as well as digits. <br>
> * `"column1_name"` and `"column2_name"` are `column arguments`. They can contain small letters, digits and `'_'` symbols. They represent the column name of the table, and will be assigned an INTEGER data type in the table. <br>
> * `"ForeignTableName_id"` is a `foreign key argument`. These arguments must end with an `"_id"` suffix. They must be capitalized and can contain small and capital letters, as well as digits, same as for `table name argument`. The part before the `"_id"` should reference a table name. After the SQL is generated, the table (`Table1Name`) will have a foreign key `foreigntablename_id` pointing to a column `foreigntablename_id` of the `ForeignTableName` table. <br>

***Note before using:***
>  * If `table name argument` isn't capitalized, the script will do it
> automatically. Also, it will remove any `'_'` characters from it as well.<br>
>  * If `column argument` contains any capital letters, running the script
> will replace them with their lower case counterparts. <br>
>  * Part of the `foreign key argument` before the `"_id"` will be treated as if it was a `table name argument` (Explained above). <br>
>
> These changes will be present in both the `create-db.sql` file and the `sorted-in.txt` file.<br>
> Check the `log.txt` file for the verbose explanations on these and other user mistakes, and for the script failures.
