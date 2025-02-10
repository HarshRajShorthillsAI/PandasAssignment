import pandas as pd
import numpy
import os
from pathlib import Path

class ReadData:

    def __init__(self, folder_path:str):
        self.folder_path = folder_path
        self.resultant_dataframe = pd.DataFrame()

    def concatenate_data(self, files:list[str])->None:
        # read these files as dataframe and concatenate them to resultant dataframe
        for file in files:
            if file.endswith('.tsv.gz'):
                data = pd.read_csv(f"{self.folder_path}/{file}", compression='infer', header=None, on_bad_lines='skip', delimiter='\t')
            else:
                continue
            print(f"Data from {self.folder_path}/{file}")
            self.analyze_dataframe(data)
            self.resultant_dataframe = pd.concat([self.resultant_dataframe, data], axis=0, ignore_index=True)

            del data
    
    def load_zipped_data(self)->None:
        # create empty dataframe
        self.resultant_dataframe = pd.DataFrame()

        # list the files in the data folder
        files = os.listdir(self.folder_path)

        # read these files as dataframe and concatenate them to resultant dataframe
        self.concatenate_data(files)

        # basic stats for resultant dataframe
        if self.resultant_dataframe.empty == False:
            self.analyze_dataframe(self.resultant_dataframe)

    @classmethod
    def load_new_zipped_data(self, stored_dataframe_file:str, used_files:str)->None:
        # Read files list of data folder content
        files_list = os.listdir(self.folder_path)
        
        stored_data = None

        # Check if the resultant dataframe file is stored in the data folder
        if Path(f"./Data/{stored_dataframe_file}").exists() == True:
            stored_data = pd.read_csv(f"{self.folder_path}/{stored_dataframe_file}", header=None, on_bad_lines='skip', delimiter='\t')
        else:
            stored_data = pd.DataFrame()

        # list of files that are already read and concatenated to resultant dataframe
        read_files_list = []

        # check if there is concatenated dataframe list file available 
        if Path(f"./Data/{used_files}").exist() == False:
            Path.touch(f"./Data/{used_files}")

        # open the concatenated dataframe list file
        with open(f"./Data/{used_files}", "r") as output:
            read_files_list = list(output.read())
        
        # derive the list of files that are not concatenated in the resultant file
        unread_list = [item for item in files_list if item not in read_files_list]

        # append those new dataframes to resultant dataframe
        for file in unread_list:
            data = pd.read_csv(f"{self.folder_path}/{file}", compression='infer', header=None, on_bad_lines='skip', delimiter='\t')
            print(f"Data from {self.folder_path}/{file}")
            self.analyze_dataframe(data)
            stored_data = pd.concat([stored_data, data], axis=0)
            del data

        # show basic stats for the resultant dataframe
        self.analyze_dataframe(stored_data)

    @classmethod
    def analyze_dataframe(cls, data:pd.DataFrame)->None:
        print(f"Resultant dataframe after concatenation:\n{data.head(10)}\ndataframe shape:{data.shape}\n")
        print(f"Resultant dataframe stats:\n{data.describe()}")