from DB_layer import *
import pandas as pd

excel_file_path="Simplified Data - Draft I.xlsx"

df=pd.read_excel(excel_file_path)

mult_str="""INSERT INTO payment ( paiementsNom
      ,paiementsType
      ,somme
      ,date
      ,comment) VALUES"""

for idx,row in enumerate(df.iterrows()):
    #print(df.iloc[idx]["Amount"])
    mult_str=mult_str+"('{0}','Charges Fixes',{1},'{2}','{3}'),".format(df.iloc[idx]["Recipient"],df.iloc[idx]["Amount"],str(df.iloc[idx]["Date"]).split(" ")[0],df.iloc[idx]["Comment"])


print(mult_str)

insert_into_table(mult_str)





