import pandas as pd
import gc
import os
from pathlib import Path

class ReadData:

    def __init__(self, folder_path:str):
        self.folder_path = folder_path
        self.resultant_dataframe = pd.DataFrame()

    def read_files(self, filename:str, verbose:bool)->pd.DataFrame:
        assert filename in os.listdir(self.folder_path), "File not found in directory path specified."
        data_frame = pd.read_csv(f"{self.folder_path}/{filename}", delimiter='\t', header=None, compression='infer', on_bad_lines='skip')
        self.analyze_dataframe(data_frame)
        return data_frame

    def concatenate_data(self, data:pd.DataFrame, verbose:bool)->None:
        self.resultant_dataframe = pd.concat([self.resultant_dataframe, data], axis=0, ignore_index=True)
        print(f"dataframe memory: {self.resultant_dataframe.info(memory_usage='deep')}")
        gc.collect()
    
    def list_files(self)->list[str]:
        return os.listdir(self.folder_path)

    def load_zipped_data(self, verbose:bool)->None:
        files = self.list_files()

        for file in files:
            data = None
            if file.endswith('.tsv.gz'):
                data = self.read_files(filename=file, verbose=verbose)
            else:
                continue
            print(f"Data from {self.folder_path}/{file}")
            
            if verbose:
                self.analyze_dataframe(data)

            # read these files as dataframe and concatenate them to resultant dataframe
            self.concatenate_data(data)

            del data
            gc.collect()

    def analyze_dataframe(self, data:pd.DataFrame)->None:
        assert data.empty == False, "Cannot analyze empty dataframe"

        print(f"Data from dataframe:\n{data.head(10)}\ndataframe shape:{data.shape}\n")
        print(f"Resultant dataframe stats:\n{data.info()}")