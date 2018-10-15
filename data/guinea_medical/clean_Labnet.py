import pandas as pd
import os
from operator import is_not
from functools import partial


#file ='Labnet_Edited.csv'
file = '../../guinea_healthcare_table.csv'




fileout = file.replace('.csv','_cleaned.csv')
data =pd.read_csv(file,encoding='windows-1252')
new_col = {col:col.replace(' / ','_').replace(' ','_').lower() for col in data.columns}
data.rename(columns=new_col,inplace=True)
data.rename(columns = {'widal_(fever)':'widal',
                       'hb_(sahli)_(hemoglobin)':'hb_sahli',
                       '1':'training_1',
                        '2':'training_2',
                        '3':'training_3',
                        '4':'training_4',
                        '5':'training_5'
                       },inplace=True)
try:
    data.drop(columns='unnamed:_0',inplace=True)
except:
    pass
print(data.columns)


def check_public_private(data):
    for row in data.index:
        value = data.loc[row,'public_private']
        if pd.notnull(data.loc[row,'public_private']):
            data.loc[row,'public_private'] = value.lower().strip()
    return data

def check_region(data):
    for row in data.index:
        value = data.loc[row,'region']
        if pd.notnull(data.loc[row,'region']):
            data.loc[row,'region'] = value.lower().strip().replace('è','e').replace('ë','e').replace('é','e')
    return data

def check_prefecture(data):
    for row in data.index:
        value = data.loc[row,'prefecture']
        if pd.notnull(data.loc[row,'prefecture']):
            data.loc[row,'prefecture'] = value.lower().strip().replace('è','e').replace('ë','e').replace('é','e')
    return data

def check_affiliation(data):
    for row in data.index:
        value = data.loc[row,'affiliation']
        if pd.notnull(data.loc[row,'affiliation']):
            data.loc[row,'affiliation'] = value.lower().strip()
    return data

def check_name(data):
    for row in data.index:
        value = data.loc[row,'name_of_laboratory']
        if pd.notnull(data.loc[row,'name_of_laboratory']):
            data.loc[row,'name_of_laboratory'] = value.lower().strip().replace('è','e').replace('ë','e').replace('é','e')
    return data

def check_training(data):
    for row in data.index:
        for col in ['training_1', 'training_2', 'training_3', 'training_4','training_5']:
            value = data.loc[row,col]
            if pd.notnull(data.loc[row,col]):
                data.loc[row,col] = value.lower().strip()
                if value.lower().strip()=='-':
                    data.loc[row,col]=None
                if value.lower().strip()=='bcciloscopie':
                    data.loc[row,col]='bacilloscopy'
                if value.lower().strip()=='sérélogie':
                    data.loc[row,col]='serology'
                if value.lower().strip()=='bcciloscopie tb':
                    data.loc[row,col]='bacilloscopy tuberculosis'
                if value.lower().strip() == 'bacteériologie':
                    data.loc[row, col] = 'bacteriology'
                if value.lower().strip() == 'biomol':
                    data.loc[row, col] = 'molecular biology'
                if value.lower().strip() == 'sero immunology':
                    data.loc[row, col] = 'sero-immunology'
                if value.lower().strip() == 'tubrculose':
                    data.loc[row, col] = 'bacilloscopy tuberculosis'

    return data

def check_access(data):
    for row in data.index:
        for col in ['phone', 'fax', 'computer', 'internet','tdr_palu','tdr_hiv','widal','hb_sahli','electricity_existence']:
            value = data.loc[row,col]
            if pd.notnull(data.loc[row,col]):
                if value.lower().strip()=='yes':
                    data.loc[row,col] = 1
                if value.lower().strip()=='no':
                    data.loc[row,col]= 0

    return data

def check_replacecharset(data):
    for row in data.index:
        for col in data.columns:
            value = data.loc[row,col]
            if (pd.notnull(data.loc[row,col])) and (type(value)==str):
                if 'é' in value:
                    data.loc[row,col]=data.loc[row,col].replace('é','e')
    return data

def create_hierarchy(data):
    for row in data.index:
        if pd.notnull(data.loc[row, 'name_of_laboratory']):
            data.loc[row,'hierarchy'] = 'Guinea.'+\
                                    data.loc[row,'region'].replace(' ','_') + "."+\
                                    data.loc[row, 'prefecture'].replace(' ','_') + "."+\
                                    data.loc[row, 'name_of_laboratory'].replace(' ','_')
    print(data['hierarchy'])
    return data

def combine_training(data):
    for row in data.index:
        data.loc[row,'training'] = ",".join(data.loc[row,['training_1', 'training_2', 'training_3', 'training_4','training_5']].astype(str).tolist())

    return data


data = check_public_private(data)
data = check_region(data)
data = check_prefecture(data)
data = check_affiliation(data)
data = check_training(data)
data = check_access(data)
data = check_name(data)
data = combine_training(data)
data = create_hierarchy(data)
data = check_replacecharset(data)
data.to_csv(fileout,index=None)