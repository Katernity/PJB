import json
import csv
import fileman

# Note: this requires the relevant field names to e listed below. Edit this file if new ones must be added or deleted.
# Note: the 100.00 percents turn into integers.

fileman.createfolders("out")

f = open('support_files/records.json')
data = json.load(f)

with open('out/records.csv', 'w',  encoding='UTF8', newline='') as fout:
    writer = csv.DictWriter(fout, fieldnames=["ftp_number", "identifier", "manifest",
                            "pctComplete", "process_status", "processdate", "txtName", "PJB_status"], extrasaction='ignore')
    writer.writeheader()
    writer.writerows(data)
    print("csv created")
