import json
import sys

# For early stage testing
# print(sys.argv[1])

# Parse original JSON (would be here)
parsed_json = json.loads(sys.argv[1])
print(json.dumps(parsed_json, indent=4, sort_keys=True))

# Generates new json file
x =  '{ "name":"John", "age":30, "city":"New York"}'
with open('data.json', 'w') as outfile:
    json.dump(x, outfile)
