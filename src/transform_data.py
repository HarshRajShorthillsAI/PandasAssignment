from read_data import ReadData
import pandas as pd
import numpy as np

class TransformData:

    @classmethod
    def filter_rows_by_string(cls, readData:ReadData, patternstr:str):
        print(readData.resultant_dataframe.convert_dtypes())

        readData.resultant_dataframe.rename(columns={0:'date',1:'posteventlist',2:'postproductlist',3:'link'},inplace=True)
        
        filtered_rows = readData.resultant_dataframe[readData.resultant_dataframe.iloc[:,1].str.contains(patternstr, regex=True, na=False)]
        
        print(f"Filtered rows for pattern string:\n{filtered_rows}")