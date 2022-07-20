import csv
import json
import fileman

fileman.createfolders("out")

data = []
with open('support_files/records.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",")
    for rows in reader:
        newdata = data.append(rows)
fout = open("out/records.json", "w")
prettylist = json.dumps(data, sort_keys=True, indent=4)
print(prettylist, file=fout)
print("CSV to records.json complete.")
fout.close()
