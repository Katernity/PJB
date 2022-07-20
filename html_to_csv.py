import csv
import json
import os
import fileman

from datetime import datetime
my_date = datetime.now()
date_string = my_date.strftime('%Y-%m-%d')

fileman.createfolders('out')

f = open('support_files/records.json')
records = json.load(f)

csv_list = []

# check if the nids are in the dictionary, and if so open the doc file
with open('support_files/nid_list.txt', 'r') as file:
    nid_list = file.read().splitlines()
    for nid in nid_list:
        found = False
        for record in records:
            if nid == (record['identifier']) and (record['PJB_status']) != 'Ingested':
                csv_dict = {}
                csv_dict["nid"] = nid
                csv_dict["ftp_number"] = (record['ftp_number'])
                csv_list.append(csv_dict)
                found = True
                break
        if found == False:
                print("Nid '"+nid+"' not found in records.json, or was already Ingested!")
    print(csv_list, "...looking for content files.")
f.close()
new_csv_list = []
for csv_dict in csv_list:
    filepath = "PJB-ready/"+csv_dict['ftp_number']+'_'+csv_dict['nid']+'_content.html'
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            data = file.read()
            csv_dict["document_body"] = data
            new_csv_list.append(csv_dict)
            print(f"{csv_dict['nid']} found")
    else:
        print("No html content file exists for", csv_dict['nid'])
#print(new_csv_list)
f.close()

# create the csv, given today's date
with open('out/'+date_string+'_new_document_upload_for_PJB.csv', 'w',  encoding='UTF8', newline='') as fout:
    writer = csv.DictWriter(
        fout, fieldnames=["nid", "document_body"], extrasaction='ignore')
    writer.writeheader()
    writer.writerows(new_csv_list)
    print("csv created")
