# list files/folders (listqty) at a time, buttons select/navigate
import os
import time
import RPi.GPIO as GPIO
import ioconfig
import navfolders

#establish root directory
rootdir = '/home/pi/Music'


#establish list of classes to be used for each file directory
directory=list()
for z in range(20):
    directory.append(z)

#first in list of classes is root file directory, list first items in root dir
i=0
directory[i]=Navfolders()
directory[i].listitems(4)

# start program!
if __name__== '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

'''    
request=1
while request>0 and request<8:
    print '\n'
    request=input('Select: "1"-"4" or Navigate Forward="5" Back="6" or Back a directory "7"\n')
    
# print next 4 items in list   
    if request==5 or request==6:
        directory[i].navigatelist(request)


# select folder/file: if folder, run class for that directory path
#                     if file, run mplayer?
    elif request==1 or request==2 or request==3 or request==4:
        selection=os.path.join(os.path.abspath(directory[i].currentdir),directory[i].mergelist[directory[i].list_index+request-1])
        i+=1
        
        if os.path.isdir(selection):
            rootdir=selection
            directory[i]=navfolders()
            directory[i].listitems(4)
            
        elif os.path.isfile(selection):
            print  'this is file!!'
        
# navigate back one directory
    elif request==7:
        if i>0:
            i-=1
            directory[i].listitems(4)
        else: directory[i].listitems(4)
'''