import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from rpy2.robjects import pandas2ri
import rpy2.robjects.vectors as rvectors

# Activate the automatic conversion of R objects to pandas objects
pandas2ri.activate()

# Create a function to handle the creation and use of the personal library path
def set_r_personal_lib():
    robjects.r('''
        # Set the personal library path
        user_lib <- Sys.getenv("R_LIBS_USER")

        # If the personal library path does not exist, create it
        if (!dir.exists(user_lib)) {
            dir.create(user_lib, recursive = TRUE)
        }

        # Add the personal library to the library paths
        .libPaths(c(user_lib, .libPaths()))

        # Return the library path being used
        user_lib
    ''')
    return robjects.r('user_lib')[0]

# Set the personal library path
user_lib_path = set_r_personal_lib()

# Install required packages if they are not already installed
utils = rpackages.importr('utils')
utils.chooseCRANmirror(ind=1)  # Select the first mirror in the list

required_packages = ['czso', 'dplyr', 'stringr']

for package in required_packages:
    if not rpackages.isinstalled(package):
        user_lib_path_vector = rvectors.StrVector([user_lib_path])
        utils.install_packages(package, lib=user_lib_path_vector)

# Now try to import the packages
czso = rpackages.importr('czso')

# Function to retrieve a table and save it as a CSV file
def get_table_and_save_to_csv(table_id, file_name, schema_file_name):
    try:
        # Retrieve the table from CZSO
        table = robjects.r(f'czso::czso_get_table("{table_id}")')
        table_df = pandas2ri.rpy2py(table)

        table_schema = robjects.r(f'czso::czso_get_table_schema("{table_id}")')
        schema_df = pandas2ri.rpy2py(table_schema)

        # Write the DataFrame to a CSV file
        table_df.to_csv(file_name, index=False)
        schema_df.to_csv(schema_file_name, index=False)

        print(f"Table {table_id} has been written to {file_name} and it's schema in {schema_file_name}")

    except Exception as e:
        print(f"Failed to retrieve table {table_id}: {e}")
# Retrieve and save the two tables
