import pandas as pd

# create a DataFrame with a single row of zeros
df = pd.DataFrame(data=[[0]*5], columns=['col1', 'col2', 'col3', 'col4', 'col5'])

# print the DataFrame
print(df)