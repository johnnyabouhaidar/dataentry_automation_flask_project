from DB_layer import *
import pandas as pd

excel_file_path="newdata\Simplified Data - Frais Matériel Médical - Nov & Dec.xlsx"

df=pd.read_excel(excel_file_path)
mult_str="""INSERT INTO fraismateriel ( fraismaterielnom
      ,fraismaterieltype
      ,fraismaterielsomme
      ,fraismaterieldate
      ,comment) VALUES"""

for idx,row in enumerate(df.iterrows()):
    #print(df.iloc[idx]["Amount"])
    #print(df.iloc[idx]["Comment"])
    if str(df.iloc[idx]["Comment"])=='nan':
        mult_str=mult_str+"('{0}','{4}',{1},'{2}','{3}'),".format(df.iloc[idx]["Recipient"].replace("'",""),df.iloc[idx]["Amount"],str(df.iloc[idx]["Date"]).split(" ")[0],"",df.iloc[idx]["Type"])
    else:
        mult_str=mult_str+"('{0}','{4}',{1},'{2}','{3}'),".format(df.iloc[idx]["Recipient"].replace("'",""),df.iloc[idx]["Amount"],str(df.iloc[idx]["Date"]).split(" ")[0],df.iloc[idx]["Comment"],df.iloc[idx]["Type"])


'''
mult_str="""INSERT INTO payment ( paiementsNom
      ,paiementsType
      ,somme
      ,date
      ,comment) VALUES"""

for idx,row in enumerate(df.iterrows()):
    #print(df.iloc[idx]["Amount"])
    #print(df.iloc[idx]["Comment"])
    if str(df.iloc[idx]["Comment"])=='nan':
        mult_str=mult_str+"('{0}','{4}',{1},'{2}','{3}'),".format(df.iloc[idx]["Recipient"].replace("'",""),df.iloc[idx]["Amount"],str(df.iloc[idx]["Date"]).split(" ")[0],"",df.iloc[idx]["Type"])
    else:
        mult_str=mult_str+"('{0}','{4}',{1},'{2}','{3}'),".format(df.iloc[idx]["Recipient"].replace("'",""),df.iloc[idx]["Amount"],str(df.iloc[idx]["Date"]).split(" ")[0],df.iloc[idx]["Comment"],df.iloc[idx]["Type"])
'''
'''
mult_str="""INSERT INTO facturation ( facturationNom
      ,facturationType
      ,somme
      ,date
      ,comment) VALUES"""

for idx,row in enumerate(df.iterrows()):
    #print(df.iloc[idx]["Amount"])
    #print(df.iloc[idx]["Comment"])
    if str(df.iloc[idx]["Comment"])=='nan':
        mult_str=mult_str+"('{0}','{4}',{1},'{2}','{3}'),".format(df.iloc[idx]["Recipient"].replace("'",""),df.iloc[idx]["Amount"],str(df.iloc[idx]["Date"]).split(" ")[0],"",df.iloc[idx]["Type"])
    else:
        mult_str=mult_str+"('{0}','{4}',{1},'{2}','{3}'),".format(df.iloc[idx]["Recipient"].replace("'",""),df.iloc[idx]["Amount"],str(df.iloc[idx]["Date"]).split(" ")[0],df.iloc[idx]["Comment"].replace("'",""),df.iloc[idx]["Type"])
        
'''
'''
mult_str="""INSERT INTO encaissement ( encaissementNom
      ,banque
      ,montant
      ,encaissementDate
      ,comment) VALUES"""

for idx,row in enumerate(df.iterrows()):
    #print(df.iloc[idx]["Amount"])
    #print(df.iloc[idx]["Comment"])
    if str(df.iloc[idx]["Comment"])=='nan':
        mult_str=mult_str+"('{0}','{4}',{1},'{2}','{3}'),".format(df.iloc[idx]["Encaissement Name"].replace("'",""),df.iloc[idx]["Amount"],str(df.iloc[idx]["Date"]),"",df.iloc[idx]["Banque"])
    else:
        mult_str=mult_str+"('{0}','{4}',{1},'{2}','{3}'),".format(df.iloc[idx]["Encaissement Name"].replace("'",""),df.iloc[idx]["Amount"],str(df.iloc[idx]["Date"]),df.iloc[idx]["Comment"].replace("'",""),df.iloc[idx]["Banque"])
'''

mult_str = mult_str[:-1] + ";"
print(mult_str)

insert_into_table(mult_str)





