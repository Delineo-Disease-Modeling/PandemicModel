import json

x =  '{ "name":"John", "age":30, "city":"New York"}'

with open('data.json', 'w') as outfile:
    json.dump(x, outfile)
