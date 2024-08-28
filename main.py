from fetch_czso import get_table_and_save_to_csv
from catalog import get_catalog
from translate_csv import  translate_csv_with_schema

#get_catalog("catalog.csv")


TABLE_ID = "110079"

get_table_and_save_to_csv(TABLE_ID, f"czso_table_{TABLE_ID}.csv", f"czso_schema_{TABLE_ID}.csv")

translate_csv_with_schema(f"czso_table_{TABLE_ID}.csv", f"czso_schema_{TABLE_ID}.csv", f"czso_table_{TABLE_ID}_english.csv")

