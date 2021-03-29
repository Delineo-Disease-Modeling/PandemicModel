import json
import sys

print(sys.argv[1])
# Parse original JSON (would be here)



# Generates new json file
x =  '{ "name":"John", "age":30, "city":"New York"}'
with open('data.json', 'w') as outfile:
    json.dump(x, outfile)
