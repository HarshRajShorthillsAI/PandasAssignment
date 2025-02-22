from read_data import ReadData
from transform_data import TransformData

class ETLPipeline:
    def __init__(self, folder_path:str):
        self.read_data = ReadData(folder_path, False)
        self.transform_data = TransformData(self.read_data, True)

    def task3(self):
        self.read_data.load_zipped_data()
        self.transform_data.rename_dataframe_cols()
        self.transform_data.filter_rows_by_string(pattern_str=r'20113')
        self.transform_data.create_productlist_dataframe()
        self.transform_data.store_dataframe_as_tsv()

    def task4(self):
        self.transform_data.create_dealer_ad_impression_count_from_postproductlist()

    def task5(self):
        self.transform_data.count_impressions_groupby()

    def task6(self):
        files = self.read_data.list_files()

        for file in files:
            if file.endswith('.py'):
                continue
            print(f"file: {file}")
            self.transform_data.readData.resultant_dataframe = self.read_data.read_files(file)
            self.transform_data.filter_rows_by_string('20113')
            self.transform_data.create_productlist_dataframe()
            self.transform_data.create_dealer_ad_impression_count_from_postproductlist()
            self.transform_data.get_product_model_by_evar('117')