# imports
import sys
import pandas as pd
from sqlalchemy import create_engine

def standardize_text(df,text_field):
    df[text_field] = df[text_field].str.replace(r"http\S+", "")
    df[text_field] = df[text_field].str.replace(r"http", "")
    df[text_field] = df[text_field].str.replace(r"@\S+", "")
    df[text_field] = df[text_field].str.replace(r"[^A-Za-z0-9(),!?@\'\`\"\_\n]", " ")
    df[text_field] = df[text_field].str.replace(r"@", "at")
    df[text_field] = df[text_field].str.lower()
    return df

def load_data(messagesFilePath, categoriesFilePath):
    """
    - Takes inputs as two CSV files
    - Imports them as pandas dataframe.
    - Merges them into a single dataframe

    Args:
    messagesFilePath str: Messages CSV file
    categoriesFilePath str: Categories CSV file

    Returns:
    merged_df pandas_dataframe: Dataframe obtained from merging the two input\
    data
    """

    messages    = pd.read_csv(messagesFilePath)
    categories  = pd.read_csv(categoriesFilePath)
    
    df          = messages.merge(categories, on='id')
    standardize_text(df,message)
    return df

def clean_data(df):
    """
    - Cleans the combined dataframe for use by ML model
    
    Args:
    df pandas_dataframe: Merged dataframe returned from load_data() function

    Returns:
    df pandas_dataframe: Cleaned data to be used by ML model
    """

    # Split categories into separate category columns
    categories          = df['categories'].str.split(";", expand = True)
    
    # select the first row of the categories dataframe
    firstRow            = categories.iloc[0,:].values
    
    # use this row to extract a list of new column names for categories.
    newColumns          = [col[:-2] for col in firstRow]

    # rename the columns of `categories`
    categories.columns  = newColumns

    # Convert category values to just numbers 0 or 1.
    for category in categories:

        # set each value to be the last character of the string
        categories[category]    = categories[category].str[-1]
        
        # convert column from string to numeric
        categories[category]    = pd.to_numeric(categories[category])
    
    # drop the original categories column from `df`
    df.drop('categories', axis  = 1, inplace = True)

    # concatenate the original dataframe with the new `categories` dataframe
    df[categories.columns]      = categories

    # drop duplicates
    df.drop_duplicates(inplace  = True)

    return df

def save_data(df, databaseFilePath):
    """
    Saves cleaned data to an SQL database

    Args:
    df pandas_dataframe: Cleaned data returned from clean_data() function
    database_file_name str: File path of SQL Database into which the cleaned\
    data is to be saved

    Returns:
    None
    """
    
    sqlApp          = create_engine('sqlite:///{}'.format(databaseFilePath))

    # extract file name from the file path
    dbFileName      = databaseFilePath.split("/")[-1]

    table           = dbFileName.split(".")[0]
    df.to_sql(table, sqlApp, index=False, if_exists = 'replace')


def main():
    
    if len(sys.argv) == 4:

        messagesFilePath, categoriesFilePath, databaseFilePath = sys.argv[1:]

        df = load_data(messagesFilePath, categoriesFilePath)

        df = clean_data(df)
        
        save_data(df, databaseFilePath)
        
        print('Data is formatted and saved into a database\n')
    
    else:
        print('Invalid Arguments.\nPlease provide all - 1) Messages File Path, 2) Categories File Path, 3) Database File Path\n')

if __name__ == '__main__':
    main()