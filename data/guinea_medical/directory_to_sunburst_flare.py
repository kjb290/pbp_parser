import os
import json
import pandas as pd
import pprint

def dict_value(dict_name,name):
    dict_name["name"] = name
    dict_name["children"] = []
    return dict_name["children"]


data = pd.read_csv('labnet_updated.csv')

initial_name = [[data.loc[item,'id'].split('.')[0],item] for item in data.index if len(data.loc[item,'id'].split('.'))==1]
data_json = [{"name":initial_name[0][0],
             "fullname":data.loc[initial_name[0][1],'name'],
             "dept":data.loc[initial_name[0][1],'dept'],
             "div": data.loc[initial_name[0][1], 'div'],
             "office": data.loc[initial_name[0][1], 'office'],
             "size":1,
              "children":[]}]


print(data_json)

for ind_index,index in enumerate(data.index):
    if ind_index>-1:
        hierarchy = data.loc[index,'id'].split('.')
        temp=data_json
        if len(hierarchy)!=1:
            for ind, loc in enumerate(hierarchy):
                name_match = [item_ind for item_ind, item in enumerate(temp) if loc == item["name"]]
                if not name_match:
                    temp.append({"name":loc,
                                 "fullname":data.loc[index,'name'],
                                 "dept":data.loc[index,'dept'],
                                 "div": data.loc[index, 'div'],
                                 "office": data.loc[index, 'office'],
                                 "size":1,
                                 "children":[]})
                    name_index =0
                    temp = temp[name_index]['children']
                else:
                    name_index = name_match[0]
                    temp = temp[name_index]['children']

final = data_json[0]
pprint.pprint(final)
with open('arl_org_flare.json','w') as f:
    f.write(json.dumps(final))
f.close()

'''print(loc)
if loc not in [item['name'] for item in temp]:
    temp = dict_value(temp,loc).append({"name":loc})

    print(data_json)
'''