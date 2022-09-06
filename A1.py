#!/usr/bin/env python
# coding: utf-8


import pandas as pd
from itertools import islice


path='~/Desktop/Research Associate Assignment/Research-Aptitude-Test-Data/Q1_Dataset.xlsx'
df = pd.read_excel(path)

df.drop(df.columns.difference(['gvkey', 'fyear', 'csho', 'prcc_f', 'pstkl', 'lct', 'at', 'invt', 'dltt', 'xrd', 'naics', 'sic']), 1, inplace=True)
df.rename(columns={'at': 'att'}, inplace=True)
df = df[df.att != 0.0]
df = df.dropna()
df = df.drop_duplicates()
df = df.reset_index(drop=True)

print(df.head())

df['tq'] = df.apply(lambda row: (((row['csho']*row['prcc_f']) + row['pstkl'] + row['lct'] - row['att'] + row['invt'] + row['dltt'])/row['att']), axis=1)

corr_mat = df.corr()

print("Correlation between R&D and tq is: ", round(corr_mat['xrd']['tq'], 2))

industries = df['naics'].unique().tolist()
fyears = df['fyear'].unique().tolist()
print(fyears)


cols = ['naics', 'corr']
corr_industries = pd.DataFrame(columns=cols)
for i in range(len(industries)):
    row_df = pd.DataFrame([[industries[i], round((df.loc[df.naics==industries[i]]).corr()['xrd']['tq'], 2)]], columns=cols)
    corr_industries = pd.concat([corr_industries, row_df])

#df.loc[(df['naics'] == 334416) & (df['fyear'] == 2010)]

corr_by_time_industry = { }
for i in fyears:
    corr_by_time_industry[i] = { }
    for j in industries:
        correlation = round((df.loc[(df['fyear'] == i) & (df['naics'] == j)]).corr()['xrd']['tq'], 2)
        corr_by_time_industry[i][j] = correlation if pd.isna(correlation)==False else "not interpretable"

#dict(islice(corr_by_time_industry.items(), 0, 2))
print(corr_by_time_industry[2010])