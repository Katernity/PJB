import urllib.request
import csv
import json
import os
import sys
import fileman

# for "bond" or "king" you can run this with a parameter
# python web_csv_json.py bond
# or if you don't include the parameter, terminal will display acceptable names from the constellation

if os.path.exists("support_files/constellation_dict.json"):
    print("Dictionary found in support files! Please enter a name from the list")
    f = open('support_files/constellation_dict.json')
    data = json.load(f)
    SNAC_people = data
else:
    print("No dictionary found: please pick a name from the hardcoded pair.")
    SNAC_people = {
        "bond": "https://snaccooperative.org/download/83834110?type=constellation_json",
        "king": "https://snaccooperative.org/download/83213963?type=constellation_json",
    }


try:
    print('cmd entry:', sys.argv)
    name = sys.argv[1]
    type(name) == str
    print("Name accepted from terminal.")
except:
    print(SNAC_people.keys())
    name = input("Type a name from available keys above\n")
if not name in SNAC_people:
    raise TypeError("Accepted key not used")


fileman.createfolders(f"out/{name}")

url = SNAC_people.get(name)

# Open the url of the person indicated
webUrl = urllib.request.urlopen(url)
print("result code: " + str(webUrl.getcode()))
data = webUrl.read()
data = json.loads(data)
data = data['relations']

# for each dictionary within the list, this navigates one level deep and copies a new key/value pair onto the first layer to de-nest.
for dictionary in data:
    term = dictionary["targetEntityType"]["term"]
    dictionary.update({"classification": term})

    # This also retrieves a new dictionary of people and their urls, so they can also be downloaded by typing their names.
    SNAC_people.update({dictionary["content"]: "https://snaccooperative.org/download/" +
                        dictionary["targetConstellation"]+"?type=constellation_json"})
with open('out/'+name+'/constellation_dict.json', 'w',  encoding='UTF8', newline='') as f:
    SNAC_people = json.dumps(SNAC_people, indent=4)
    f.writelines(SNAC_people)
    print("--created a new dictionary based on the constellation relations")
# This matches fieldnames from the key, and return the values into a csv.
with open('out/'+name+'/people_and_orgs.csv', 'w',  encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[
                            "content", "targetArkID", "classification", "targetConstellation"], extrasaction='ignore')
    writer.writeheader()
    writer.writerows(data)
    print("--created csv file")
    print(f"Output will be located in subfolder 'out/{name}'")
