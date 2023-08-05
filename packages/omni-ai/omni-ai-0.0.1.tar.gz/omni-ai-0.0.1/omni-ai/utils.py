from typing import List
from IPython.display import display
from termcolor import colored
import pandas as pd


class Utils:
    def __init__(self):
        pass

    def get_categorical_columns(self, df) -> list:
        '''
        Return list of categorical features
        '''
        return df.select_dtypes(include="O").columns.tolist()

    def get_numerical_columns(self, df) -> list:
        '''
        Return list of numerical features
        '''
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        num_col = df.select_dtypes(include=numerics).columns
        return num_col

    def shape(self, df, formatted_output=True) -> None:
        if not formatted_output:
            print("Shape of DataFrame: ", df.shape)
            return
        print(
            colored(f"Dataframe contains {df.shape[0]} rows and {df.shape[1]} columns", "blue", attrs=["bold"]))

    def sample(self, df, num_or_rows=10, all_columns=True) -> None:
        if all_columns:
            pd.set_option("display.max_columns", None)
        print(colored("\nSample of Dataframe:", "red", attrs=["bold"]))
        display(df.sample(num_or_rows))
