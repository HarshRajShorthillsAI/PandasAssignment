from read_data import ReadData
from transform_data import TransformData

if __name__ == "__main__":
    readData = ReadData('./Data')
    readData.load_zipped_data()
    transformData = TransformData()
    TransformData.filter_rows_by_string(readData=readData, patternstr='20113,|,20113,|,20113| 20113| 20113 |20113 ') #regex for string match