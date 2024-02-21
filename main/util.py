import ast
import pandas as pd
import constants

# defining datas
def readfile(csv_path):
    try:
        df_data=pd.read_csv(csv_path, encoding='utf-8-sig')
        return process_df(df_data)
    #exception if the file cant be found 
    except FileNotFoundError:
        print(" CSV file could not be found.")
        exit(1)
    #exception if there are issues reading the csv file
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        exit(1)

def process_df(df_data):
    # convert based on the features_datatypes
    for feature, datatype in constants.FEATURES_DATATYPES.items():
        # if feature not in the dataframe, continue
        if feature not in df_data.columns:
            continue
        if datatype == "string":
            df_data[feature] = df_data[feature].astype(str)
        elif datatype == "integer":
            df_data[feature] = pd.to_numeric(df_data[feature], errors='coerce')
        elif datatype == "float":
            df_data[feature] = pd.to_numeric(df_data[feature], errors='coerce')
        elif datatype == "dictionary":
            df_data[feature] = df_data[feature].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else x)
        elif datatype == "list":
            df_data[feature] = df_data[feature].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) and x != "nan" else x)
        elif datatype == "ISO8601":
            df_data[feature] = pd.to_datetime(df_data[feature], format='%H:%M', errors='coerce')
    # # print dtypes
    # print(df_data.dtypes)
    return df_data