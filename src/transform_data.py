from read_data import ReadData
import pandas as pd

class TransformData:

    def __init__(self, readData:ReadData):
        self.readData = readData

    def filter_rows_by_string(self, patternstr:str)->pd.DataFrame:
        self.readData.resultant_dataframe.convert_dtypes()

        self.readData.resultant_dataframe.rename(columns={0:'date',1:'posteventlist',2:'postproductlist',3:'link'},inplace=True)
        
        filtered_rows = self.readData.resultant_dataframe[self.readData.resultant_dataframe.iloc[:,1].str.contains(patternstr, regex=True, na=False)]
        
        print(f"Filtered rows for pattern string:\n{filtered_rows}")

        return pd.DataFrame(filtered_rows)

    def create_productlist_dataframe(self, dataFrame:pd.DataFrame)->pd.DataFrame:
        assert set(['postproductlist']).issubset(dataFrame.columns), "Dataframe must contain postproductlist column in it"
        dataFrame.convert_dtypes(infer_objects=True) 
        
        product_data = dataFrame.iloc[0, 2].split(';;;')
        product_index = product_data[0]
        product_features = [x for x in product_data[1].split('|')]
        product_features_split = [x.split('=', 1) for x in product_features]
        product_columns = [x[0] for x in product_features_split]

        print(product_data)
        print(product_index)
        print(product_columns)
        print(product_features)
        
        dict_features = {}
        
        for a in dataFrame.iloc[:, 2]:
            product_data = a.split(';;;')
            product_index = product_data[0]
            product_features = [x for x in product_data[1].split('|')]
            product_features_split = [x.split('=', 1) for x in product_features]
            product_values =  [x[1] if len(x)>1 else '' for x in product_features_split]

            dict_features.update({product_index: product_values})

        resultant_dataframe = pd.DataFrame.from_dict(dict_features, orient='index')

        print(f"post product list dataframe:\n{resultant_dataframe}")

        resultant_dataframe.to_csv('postproductlist20113.tsv', sep='\t')
        print(f"Dataframe saved as postproductlist20113.tsv")

        return resultant_dataframe