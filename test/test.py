import pandas as pd

class test:
    def __init__(self,data=None):
        self.dict_df = {'test':[self.read()]}
    
    def read(self,file = 'bin/real_info/Forward/neurological disoders.xlsx'):
        df = pd.read_excel(file,sheet_name='所有结果',skiprows=1)
        list_head = df.loc[:,['IDP Name','IDP ID','Tissue/Region','IDP Subtype','Disorder']]
        return list_head,df

test = test()

# def a():
#     print(test.df)

# def b():
#     print(test.df)
a,b = test.dict_df['test']
print(a)
print(b)