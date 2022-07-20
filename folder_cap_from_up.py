import sys
import fileman
import fixes

#folders
inname = "in"
outname = "out_capfix_from_upper"
    
print(f"Output to be located in subfolder out/{outname}'")
outname = str(outname)
fileman.createfolders(f'out/{outname}')

#changelog will tell you what changed, and how many things changed, and final character count. > the print statements go there.
temp = sys.stdout 
sys.stdout = open('out/changelog_infolder_capFromUpper.txt','wt')

file_list = fileman.files2list(inname)

#edit match if needed
matching = [f for f in file_list if "content.html" in f]

for fname in matching:
    print("\n...Processing "+fname+"\n")
    fout = open("out/"+outname+"/"+fname, "wt")
    with open(inname+"/"+fname, 'r') as file:
        data = file.read()
        data = fixes.basic_replaces(data)
        data = fixes.fromupper(data)
        data = fixes.capfix_fromlist(data)
        data = data.replace('\n', '') 
        fout.writelines(data)

sys.stdout = temp
print("Complete")
fout.close()
