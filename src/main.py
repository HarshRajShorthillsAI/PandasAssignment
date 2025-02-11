from read_data import ReadData
from transform_data import TransformData
import gc

if __name__ == "__main__":
    read_data = ReadData('./Data')
    read_data.load_zipped_data()
    transform_data = TransformData(readData=read_data)
    print(gc.collect())
    filtered_data = transform_data.filter_rows_by_string(patternstr=r'20113')#regex for string match
    dataframe_product_list = transform_data.create_productlist_dataframe(filtered_data)