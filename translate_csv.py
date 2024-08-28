import pandas as pd
from googletrans import Translator


# Function to translate text
def translate_text(text, src='cs', dest='en'):
    translator = Translator()
    return translator.translate(text, src=src, dest=dest).text


# Function to load schema and map descriptions to columns
def load_schema(schema_file):
    schema_df = pd.read_csv(schema_file)
    # Use the correct column names from your schema
    schema_mapping = dict(zip(schema_df['name'], schema_df['dc:description']))
    return schema_mapping


# Function to translate a CSV file using schema
def translate_csv_with_schema(input_file, schema_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Load schema
    schema_mapping = load_schema(schema_file)

    # Create a dictionary to store translated values
    translation_dict = {}

    # Translate the column headers using schema descriptions
    translated_columns = []
    columns_to_skip = set()  # Set to keep track of columns where translation should be skipped

    for col in df.columns:
        translated_desc = translate_text(schema_mapping.get(col, col), src='cs', dest='en')
        translated_columns.append(translated_desc)

        # Mark columns to skip entry translation if they contain '_kod' or translated description contains 'code'
        if '_kod' in col or "code" in translated_desc.lower():
            columns_to_skip.add(translated_desc)

    df.columns = translated_columns

    # Identify columns to translate (non-numeric columns)
    columns_to_translate = df.select_dtypes(include=['object']).columns

    # Translate only unique entries in the selected columns
    for col in columns_to_translate:
        if col not in columns_to_skip:
            unique_entries = df[col].dropna().unique()  # Get unique non-null entries
            for entry in unique_entries:
                if entry not in translation_dict:  # Only translate if not already translated
                    translation_dict[entry] = translate_text(entry)  # Translate and store in the dictionary

            # Replace the entries in the DataFrame with their translations
            df[col] = df[col].map(translation_dict)

    # Save the translated DataFrame to a new CSV file
    df.to_csv(output_file, index=False)
    print(f"Translated file saved as {output_file}")


# Translate the CSV file using its schema
translate_csv_with_schema("czso_table_110079.csv", "czso_schema_110079.csv", "czso_table_110079_english.csv")
