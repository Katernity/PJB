import fixes
import sys
import fileman

fileman.createfolders("out")

temp = sys.stdout 
sys.stdout = open('out/changelog_single_capfix_upper.txt','wt')

fout = open("out/out_capfixUpper.html", "wt")
with open('in.html', 'r') as file:
    data = file.read()
    data = fixes.basic_replaces(data)
    data = fixes.fromupper(data)
    data = fixes.capfix_fromlist(data)
    #data = data.replace('\n', '')
    fout.writelines(data)

fout.close()

sys.stdout = temp
print("Complete")