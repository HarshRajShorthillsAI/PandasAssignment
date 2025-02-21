from read_data import ReadData
import pandas as pd
import numpy as np
import gc

class TransformData:

    def __init__(self, read_data:ReadData):
        self.readData = read_data
        self.resultant_groupby = [pd.DataFrame(), pd.DataFrame()]

    def clean_dataframe(self)->None:
        self.readData.resultant_dataframe.fillna(str(''), inplace=True)
        self.readData.resultant_dataframe = self.readData.resultant_dataframe.convert_dtypes(infer_objects=True)

    def rename_dataframe_cols(self)->None:
        self.readData.resultant_dataframe.rename(columns={0:'date',1:'posteventlist',2:'postproductlist',3:'link'},inplace=True)

    def filter_rows_by_string(self, pattern_str:str)->None:
        rows = self.readData.resultant_dataframe.iloc[:, 1].astype(str).apply(lambda x: pattern_str not in x.split(','))
        index = self.readData.resultant_dataframe.index[rows]
        self.readData.resultant_dataframe.drop(index=index, inplace=True)
        
        # Concluded that splitting string into list of substrings and then searching is better option than regex search

        self.rename_dataframe_cols()

        print(f"Filtered rows for pattern string:\n{self.readData.resultant_dataframe}")

        # self.store_dataframe_as_tsv(filename="postproductlist20113.tsv.gz")

    def store_dataframe_as_tsv(self, filename:str="postproductlist20113.tsv.gz")->None: #causing memory full

        chunk_size = 150000  # Adjust if needed (lower = even less RAM usage)

        with open("chunked_saved_data.tsv", "w", encoding="utf-8") as f:
            for i, chunk in enumerate(np.array_split(self.readData.resultant_dataframe, len(self.readData.resultant_dataframe) // chunk_size + 1)):
                chunk.to_csv(f, sep="\t", index=False, header=(i == 0), mode="a")
                del chunk  # Immediately free memory

    def create_productlist_dataframe(self)->None:
        assert set(['postproductlist']).issubset(self.readData.resultant_dataframe.columns), "Dataframe must contain postproductlist column in it"
        # self.clean_dataframe(dataframe=data_frame)
        self.readData.resultant_dataframe['postproductlist'] = self.readData.resultant_dataframe['postproductlist'].astype(str).apply(lambda x: x.split(','))
        self.readData.resultant_dataframe = self.readData.resultant_dataframe.explode(['postproductlist'], ignore_index=True)
        print(f"Dataframe with all the products in separate rows:\n{self.readData.resultant_dataframe}")
        print(self.readData.resultant_dataframe['postproductlist'])
        self.readData.resultant_dataframe.drop(['date', 'link', 5], axis=1, inplace=True)
        self.readData.resultant_dataframe = self.readData.resultant_dataframe.convert_dtypes(infer_objects=True)
        print(self.readData.resultant_dataframe.info(memory_usage='deep'))
        gc.collect()

    def create_dealer_ad_impression_count_from_postproductlist(self)->None:

        # data = pd.read_csv(filename, delimiter='\t')
        print(f"columns are: {self.readData.resultant_dataframe.columns}")
        self.readData.resultant_dataframe['postproductlist'] = self.readData.resultant_dataframe['postproductlist'].astype(str)
        self.readData.resultant_dataframe['postproductlist'] = self.readData.resultant_dataframe['postproductlist'].apply(lambda x: x.split(';'))
        self.readData.resultant_dataframe = self.readData.resultant_dataframe.convert_dtypes()
        print(self.readData.resultant_dataframe)
        print(self.readData.resultant_dataframe.dtypes)
        
        self.readData.resultant_dataframe = pd.DataFrame({
            'dealer_id': self.readData.resultant_dataframe['postproductlist'].apply(lambda x: x[0] if len(x) > 0 else None),
            'ad_id': self.readData.resultant_dataframe['postproductlist'].apply(lambda x: x[1] if len(x) > 1 else None),
            'impression_count': self.readData.resultant_dataframe['postproductlist'].apply(lambda x: x[4].split('|')[0].split('=')[1] if len(x) > 4 else None),
            'rest_post_product_list': self.readData.resultant_dataframe['postproductlist'].apply(lambda x: ''.join(x[5:]) if len(x) > 4 else None),
            'domain': self.readData.resultant_dataframe[4].apply(lambda x: x.split('www.')[1].split('.')[0] if pd.notna(x) and x != '' else '')
        })

        # data.to_csv('dealeradimpression.tsv', sep='\t', mode='a', index=False) #data still NDFrame

        # del data
        gc.collect()

        print("Data appended successfully.")

    def count_impressions_groupby(self)->None:
        self.readData.resultant_dataframe['impression_count'] = pd.to_numeric(self.readData.resultant_dataframe['impression_count'], errors='coerce')
        self.readData.resultant_dataframe['dealer_id'] = pd.to_numeric(self.readData.resultant_dataframe['dealer_id'], errors='coerce')
        self.readData.resultant_dataframe.reset_index()
        self.readData.resultant_dataframe['impression_count'] = self.readData.resultant_dataframe['impression_count'].fillna(0).astype(int)
        self.readData.resultant_dataframe['domain'] = self.readData.resultant_dataframe['domain'].fillna('')
        grouped_count_by_domain = self.readData.resultant_dataframe[['domain', 'impression_count']].groupby(['domain']).sum()
        self.readData.resultant_dataframe['dealer_id'] = self.readData.resultant_dataframe['dealer_id'].fillna(0).astype(int)
        grouped_count_by_dealerid = self.readData.resultant_dataframe[['dealer_id', 'impression_count']].groupby('dealer_id').sum()

        print(f"Count of impressions groupy domain:\n{grouped_count_by_domain}")
        print(f"Count of impressions groupy dealer_id:\n{grouped_count_by_dealerid}")
        if self.resultant_groupby[0].empty:
            self.resultant_groupby[0] = grouped_count_by_domain
        else:
            self.resultant_groupby[0] += grouped_count_by_domain
        
        if self.resultant_groupby[1].empty:
            self.resultant_groupby[1] = grouped_count_by_dealerid
        else:
            self.resultant_groupby[1] += grouped_count_by_dealerid
        print(f"resultant sum of impressions grouped by domain:\n{self.resultant_groupby[0]}\n\nresultant sum of impressions grouped by dealer:\n{self.resultant_groupby[1]}")

        self.resultant_groupby[0].to_csv("impression_count_grouped_by_domain.csv", sep=',', header=None)
        self.resultant_groupby[1].to_csv("impression_count_grouped_by_dealer_id.csv", sep=',', header=None)

    def get_product_model_by_evar(self, evar: int, chunk_size: int):
        # Fill missing values and drop unnecessary columns in place
        self.readData.resultant_dataframe.fillna('', inplace=True)
        self.readData.resultant_dataframe.convert_dtypes(infer_objects=True)
        self.readData.resultant_dataframe.reset_index(inplace=True)
        self.readData.resultant_dataframe.drop(columns=['impression_count'], inplace=True, errors='ignore')

        # Split the 'rest_post_product_list' column by '|'
        self.readData.resultant_dataframe['rest_post_product_list'] = \
            self.readData.resultant_dataframe['rest_post_product_list'].apply(lambda x: x.split('|'))
        
        evar_series = []

        for y in self.readData.resultant_dataframe['rest_post_product_list']:
            found = False
            for z in y:
                if evar in z.split('='):
                    evar_series.append(z.split('=')[1])
                    found = True
                    break
            if not found:
                evar_series.append('')  # Append '' only if no match is found in the inner loop


        self.readData.resultant_dataframe = self.readData.resultant_dataframe.assign(evar_model=pd.Series(data=evar_series, index=self.readData.resultant_dataframe.index))

        print(f"new dataframe created: {self.readData.resultant_dataframe['evar_model']}")