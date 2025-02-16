import pandas as pd
import gc
import os
from pathlib import Path

class ReadData:

    def __init__(self, folder_path:str):
        self.folder_path = folder_path
        self.resultant_dataframe = pd.DataFrame()

    def concatenate_data(self, data:pd.DataFrame)->None:
        self.resultant_dataframe = pd.concat([self.resultant_dataframe, data], axis=0, ignore_index=True)
        print(f"dataframe memory: {self.resultant_dataframe.info(memory_usage='deep')}")
        gc.collect()
    
    def load_zipped_data(self)->None:
        self.resultant_dataframe = pd.DataFrame()

        files = os.listdir(self.folder_path)

        verbose = 0
        verbose = int(input("Do you want to print the data being loaded from the folder(No=0,Yes=1)"))

        for file in files:
            data = None
            if file.endswith('.tsv.gz'):
                data = pd.read_csv(f"{self.folder_path}/{file}", compression='infer', header=None, on_bad_lines='skip', delimiter='\t')
            else:
                continue
            print(f"Data from {self.folder_path}/{file}")
            
            if verbose!=0:
                self.analyze_dataframe(data)

            # read these files as dataframe and concatenate them to resultant dataframe
            self.concatenate_data(data)

            del data
            gc.collect()

        del self.folder_path

        # # basic stats for resultant dataframe
        # if self.resultant_dataframe.empty == False:
        #     self.analyze_dataframe(self.resultant_dataframe)

    def load_new_zipped_data(self, stored_dataframe_file:str, used_files:str)->None: #Not used
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

    def analyze_dataframe(self, data:pd.DataFrame)->None:
        assert data.empty == False, "Cannot analyze empty dataframe"

        print(f"Data from dataframe:\n{data.head(10)}\ndataframe shape:{data.shape}\n")
        print(f"Resultant dataframe stats:\n{data.describe()}")