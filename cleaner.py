import json 
f = open('data/coins.json')
file = json.load(f)
print(file['data']['cryptoCurrencyList'][0].keys())

for item in file['data']['cryptoCurrencyList']:
    for i in ['id', 'slug', 'tags', 'cmcRank', 'marketPairCount', 'circulatingSupply', 'selfReportedCirculatingSupply', 'totalSupply', 'maxSupply', 'isActive', 'lastUpdated', 'dateAdded', 'quotes', 'isAudited', 'platform', 'auditInfoList']:
        if i in item:
            del item[i]

with open('data/coins2.json', 'w') as data_file:
    data = json.dump(file, data_file)