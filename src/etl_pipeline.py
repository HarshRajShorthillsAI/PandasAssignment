from read_data import ReadData
from transform_data import TransformData
import os
import gc

class ETLPipeline:
    def __init__(self, folder_path:str):
        self.read_data = ReadData(folder_path)
        self.transform_data = TransformData(self.read_data)

    def run_pipeline(self):
        files = os.listdir(self.read_data.folder_path)

        verbose = input("Do you want the details of read files from folder(0:No/1:Yes): ")

        for file in files:
            gc.collect()
            if file.endswith('.py'):
                continue
            print(f"file: {file}")
            self.transform_data.readData.resultant_dataframe = self.read_data.read_files(file, verbose=verbose)
            self.transform_data.clean_dataframe()
            self.transform_data.filter_rows_by_string('20113')
            self.transform_data.create_productlist_dataframe()
            self.transform_data.create_dealer_ad_impression_count_from_postproductlist()
            self.transform_data.count_impressions_groupby()
            # del self.transform_data.readData.resultant_dataframe