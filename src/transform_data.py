from read_data import ReadData
import pandas as pd

class TransformData:

    def __init__(self, read_data:ReadData):
        self.readData = read_data

    def filter_rows_by_string(self, pattern_str:str)->pd.DataFrame:
        self.readData.resultant_dataframe.convert_dtypes()

        self.readData.resultant_dataframe.rename(columns={0:'date',1:'posteventlist',2:'postproductlist',3:'link'},inplace=True)

        filtered_rows = self.readData.resultant_dataframe[self.readData.resultant_dataframe.iloc[:,1].astype(str).apply(lambda x: pattern_str in x.split(','))]
        
        # Concluded that splitting string into list of substrings and then searching is better option than regex search

        print(f"Filtered rows for pattern string:\n{filtered_rows}")

        return pd.DataFrame(filtered_rows)

    def create_productlist_dataframe(self, data_frame:pd.DataFrame)->pd.DataFrame:
        assert set(['postproductlist']).issubset(data_frame.columns), "Dataframe must contain postproductlist column in it"
        data_frame.convert_dtypes(infer_objects=True)

        resultant_dataframe = data_frame['postproductlist'].apply(lambda x: x.split(',')).explode()

        resultant_dataframe.to_csv('postproductlist20113.tsv.gz', sep='\t', compression='gzip')
        print(f"Dataframe saved as postproductlist20113.tsv")

        return resultant_dataframe