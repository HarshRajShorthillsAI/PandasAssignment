from read_data import ReadData
from transform_data import TransformData
import gc

if __name__ == "__main__":
    readData = ReadData('./Data')
    readData.load_zipped_data()
    transformData = TransformData(readData=readData)
    print(gc.collect())
    print(transformData)
    filtered_data = transformData.filter_rows_by_string(patternstr='20113,|,20113,|,20113| 20113| 20113 |20113 ')#regex for string match
    dataframe_product_list = transformData.create_productlist_dataframe(filtered_data)