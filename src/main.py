from read_data import ReadData
from transform_data import TransformData
import gc
import pandas as pd

class Main:
    @classmethod
    def task3(cls):
        print(gc.collect())
        read_data = ReadData('./Data')
        read_data.load_zipped_data()
        transform_data = TransformData(read_data=read_data)
        transform_data.clean_dataframe()
        transform_data.rename_dataframe_cols()
        transform_data.filter_rows_by_string(pattern_str=r'20113')#regex for string match
        # transform_data.clean_dataframe()
        transform_data.create_productlist_dataframe()
        transform_data.store_dataframe_as_tsv()

    @classmethod
    def task4(cls):
        read_data = ReadData('./Data')
        transform_data = TransformData(read_data=read_data)
        transform_data.create_dealer_ad_impression_count_from_postproductlist()

    @classmethod
    def task5(cls):
        read_data = ReadData('./Data')
        transform_data = TransformData(read_data=read_data)
        transform_data.count_impressions_groupby()

if __name__ == "__main__":
    # Main.task3()
    # Main.task4()
    Main.task5()