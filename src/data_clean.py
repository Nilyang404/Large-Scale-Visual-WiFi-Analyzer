import pandas as pd

data_df_0 = pd.read_csv('merged_data_0.csv')
data_df_1 = pd.read_csv('merged_data_1.csv')

data_df_0 = data_df_0[data_df_0['gps latitude'].notna() & (data_df_0['gps latitude'] != -1.0)]
data_df_1 = data_df_1[data_df_1['gps latitude'].notna() & (data_df_1['gps latitude'] != -1.0)]

df_final = pd.concat([data_df_0, data_df_1], ignore_index=True)
df_final = df_final.drop(columns=['Unnamed: 0'])
df_final = df_final.drop_duplicates()
df_final['gps latitude'] = df_final['gps latitude'].round(6)
df_final['gps longitude'] = df_final['gps longitude'].round(6)
df_final.to_csv('final_data.csv', index=False)
print("contact all file to 1")