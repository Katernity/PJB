import fixes
import sys
import fileman

fileman.createfolders("out")

temp = sys.stdout 
sys.stdout = open('out/changelog_single_file_basic_replaces.txt','wt')

fout = open("out/out_basic_replaces.html", "wt")
with open('in.html', 'r') as file:
    data = file.read()
    data = fixes.basic_replaces(data)
    fout.writelines(data)
    #data = data.replace('\n', '')
fout.close()

sys.stdout = temp
print("Complete")