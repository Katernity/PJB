from bs4 import BeautifulSoup
import re
import os
import requests
import fileman
import json
import re
import datetime

# Download new complete content from FromThePage, and put html into an individual html document for each record.

out = "out"
fileman.createfolders(out)

# Download the json file from from the page project
if os.path.exists("support_files/records.json"):
    print("Records for content located locally: This program will download only new content.")
    f = open('support_files/records.json')
    data = json.load(f)
    records = data
else:
    print("No records for content found! This will download all content from the From The Page set.")
    records = []

date = datetime.datetime.now()
simple_date = date.strftime("%x")


# Get the json file from from the page
def get_ftpjson():
    url = "https://fromthepage.com/iiif/collection/new-content"
    response = requests.get(url)
    # save json for the new-content file to local computer
    with open(out+'/fromthepage-new.json', 'wb') as f:
        f.write(response.content)
        print("Json downloaded from", url)


# use the local json file if found.
if os.path.exists(out+'/fromthepage-new.json'):
    print("Using the Json File already downloaded from from the page.")
    f = open(out+'/fromthepage-new.json')
    data = json.load(f)

else:
    print("No Json file found! Downloading a json file from From The Page.")
    get_ftpjson()


# CODEBLOCK: Process the first json file to get the manifest urls, and save a list.
#fout = open(out+'/fromthepage_intermediate_records.txt', "wt")
with open(out+'/fromthepage-new.json', 'r') as file:
    data = file.read()
    data = json.loads(data)
    data = data['manifests']


# this chunk updates the records.json file
    new_records = []
    for ftp_dict_entry in data:
        manifest = str(ftp_dict_entry['@id'])
        pctComplete = str(ftp_dict_entry['service']['pctComplete'])
        txtName = str(ftp_dict_entry["label"])
        identifier = str(ftp_dict_entry['metadata'][0]['value'])

        found = False
        for dict_entry in records:
            if "processdate" in dict_entry:
                print("Done already!", manifest,
                      "...has already been processed.")
                dict_entry.update({"process_status": "previouslycompleted"})
                new_records.append(dict_entry)
                found = True
                break
        if found == False:
            print("New Document!", manifest, "...creating record.")
            record_entry = {}
            record_entry.update({"manifest": manifest})
            record_entry.update({"pctComplete": pctComplete})
            record_entry.update({"txtName": txtName})
            record_entry.update({"processdate": simple_date})
            record_entry.update({"identifier": identifier})
            record_entry.update({"PJB_status": "not yet uploaded"})
            record_entry.update({"process_status": "new"})
            ftp_number = re.findall("https://fromthepage.com/iiif/([0-9]*)/manifest", manifest)[0]
            record_entry.update({"ftp_number": ftp_number})
            new_records.append(record_entry)

    records = new_records
#print(records, file=fout)


print(len(records), "new records match the condition")
count = 0
for record in records:
    if record["process_status"] == "new":
        print("New document identified to be processed:", record["manifest"],)
        count += 1
        if os.path.exists(out+"/"+record['ftp_number']+"_manifest_fromthepage.json"):
            print("Using the Manifest File already downloaded from from the page.")
            f = open(out+"/"+record['ftp_number']+"_manifest_fromthepage.json")
            data = json.load(f)
            this_url = record["manifest"]
        else:
            print("No manifest found! Downloading manifest from From The Page.")
            response = requests.get(record["manifest"])
            this_url = record["manifest"]
            with open(out+"/"+record['ftp_number']+"_manifest_fromthepage.json", 'wb') as f:
                f.write(response.content)
                print(
                    "New json manifest successfully downloaded from fromthepage, FTP id is", record['ftp_number'])

        # I now have a manifest
        with open(out+"/"+record['ftp_number']+"_manifest_fromthepage.json", 'r') as file:
            data = file.read()
            data = json.loads(data)
            target_dict = data["sequences"][0]["rendering"][1]
        # Find the from the page    ID of the content for the XHTML Export
            if target_dict["label"] == "XHTML Export":
                new_url = target_dict["@id"]
                print(new_url)
                response = requests.get(new_url)

        # testing if html is already present
                if os.path.exists(out+"/"+record['ftp_number']+"_raw_fromthepage.html"):
                    print("Using the raw html file already downloaded from from the page.")
                    f = open(out+"/"+record['ftp_number']+"_raw_fromthepage.html")
                    data = f.read()
                else:
                    print("No raw html found! Downloading raw html from From The Page.")
                    with open(out+"/"+record['ftp_number']+"_raw_fromthepage.html", 'wb') as f:
                        f.write(response.content)
                        print("XHTML downloaded from From The Page, for ", record['ftp_number'])

        # open the html as soup, and collect the paragraph tags
                with open(out+"/"+record['ftp_number']+"_raw_fromthepage.html") as fp:
                    soup = BeautifulSoup(fp, 'html.parser')

                fout = open(
                    "out"+"/"+record['ftp_number']+"_"+record['identifier']+"_content.html", "a")
                content = soup.select("div[class~=page-content] p")
                content = list(content)
                myout = ""
                for p in content:
                    p = str(p)
                    myout = myout + p
                myout = myout.replace('\n', '')
                fout.write(myout)
                print("New content file created for [", record['ftp_number'], "] aka [", record['identifier'], "] \n")

                index = records.index(record)
                print(count, "of", len(records), "have completed the processs!")
                fout.close()
            else:
                print("ERROR: Perhaps the Json Structure of From the Page Manifest files has changed?")

fout = open("out"+"/records.json", "w")
prettylist = json.dumps(records, sort_keys=True, indent=4)
print(prettylist, file=fout)
print("Update complete.")
fout.close()
