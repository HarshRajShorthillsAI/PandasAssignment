from read_data import ReadData
import pandas as pd
import numpy as np
import gc

class TransformData:

    def __init__(self, read_data:ReadData):
        self.readData = read_data

    def clean_dataframe(self)->None:
        self.readData.resultant_dataframe.fillna(str(''), inplace=True)
        self.readData.resultant_dataframe = self.readData.resultant_dataframe.convert_dtypes(infer_objects=True)

    def rename_dataframe_cols(self)->None:
        self.readData.resultant_dataframe.rename(columns={0:'date',1:'posteventlist',2:'postproductlist',3:'link'},inplace=True)

    def filter_rows_by_string(self, pattern_str:str)->None:
        
        self.readData.resultant_dataframe.drop(index = self.readData.resultant_dataframe.index[self.readData.resultant_dataframe.iloc[:, 1].astype(str).apply(lambda x: pattern_str not in x.split(','))], inplace=True)
        
        # Concluded that splitting string into list of substrings and then searching is better option than regex search

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
        with open('dealeradimpression.tsv', 'w') as f:
            pass

        for chunk in pd.read_csv('chunked_saved_data.tsv', delimiter='\t', chunksize=1500000):
            print(f"columns are: {chunk.columns}")
            chunk['postproductlist'] = chunk['postproductlist'].astype(str).apply(lambda x: x.split(';'))
            chunk = chunk.convert_dtypes()
            print(chunk['postproductlist'])
            print(chunk.dtypes)
            
            data = pd.DataFrame({
                'dealer_id': chunk['postproductlist'].apply(lambda x: x[0] if len(x) > 0 else None),
                'ad_id': chunk['postproductlist'].apply(lambda x: x[1] if len(x) > 1 else None),
                'impression_count': chunk['postproductlist'].apply(lambda x: x[4].split('|')[0].split('=')[1] if len(x) > 4 else None),
                'rest_post_product_list': chunk['postproductlist'].apply(lambda x: ''.join(x[5:]) if len(x) > 4 else None),
                'domain': chunk['4'].apply(lambda x: x.split('www.')[1].split('.')[0] if pd.notna(x) and x != '' else '')
            })

            data.to_csv('dealeradimpression.tsv', sep='\t', mode='a', index=False) #data still NDFrame

            del chunk
            gc.collect()

        print("Data appended successfully.")

    def count_impressions_groupby(self)->None:
        resultant_domain = pd.DataFrame()
        resultant_dealer = pd.DataFrame()

        for chunk in pd.read_csv('dealeradimpression.tsv', delimiter='\t', chunksize=1500000):
            chunk['impression_count'] = pd.to_numeric(chunk['impression_count'], errors='coerce')
            chunk['impression_count'] = chunk['impression_count'].fillna(0)
            grouped_count_by_domain = chunk[['domain', 'impression_count']].groupby(['domain']).sum()
            # chunk['dealer_id'] = chunk['dealer_id'].fillna('')
            grouped_count_by_dealerid = chunk[['dealer_id', 'impression_count']].groupby(['dealer_id']).sum()


            print(f"Count of impressions groupy domain:\n{grouped_count_by_domain}")
            print(f"Count of impressions groupy dealer_id:\n{grouped_count_by_dealerid}")
            if resultant_domain.empty:
                resultant_domain = grouped_count_by_domain
            else:
                resultant_domain += grouped_count_by_domain
            
            if resultant_dealer.empty:
                resultant_dealer = grouped_count_by_dealerid
            else:
                resultant_dealer += grouped_count_by_dealerid
        print(f"resultant sum of impressions grouped by domain:\n{resultant_domain}\n\nresultant sum of impressions grouped by dealer:\n{resultant_dealer}")