import os

#Create folders, one or more
#example call: fileman.createfolder('folder1/folder2/folder3')
def createfolders(path):
  if not os.path.exists(path):
    os.makedirs(path)
    print(f'directories: {path} created')

#functions to make folders if they don't exist already


#if __name__ == "__main__":
#  print("Not executed")
 # something here

#here are some functions about trying to operate on every file, or specific files within a subfolder that is here. 

def listfiles(path):
    dirs = os.listdir( path )
    # This would print all the files and directories
    for file in dirs:
       print(file)

def files2list(path_in):
    isExist = os.path.exists(path_in)
    print(f"Does the directory exist? {isExist}.")

    file_list = []
    dirs = os.listdir( path_in )
    for file in dirs:
       file_list.append(file)
       print(file)
    if not isExist:
      print("Input directory not found!")
    return file_list

