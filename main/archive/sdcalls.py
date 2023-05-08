import os
import time
import navfolders


def start_sd():
    global i
    global directory
    
    os.system('clear') # clear command window
    
    #establish root directory
    rootdir = '/home/pi/Music'

    #establish list of classes to be used for each file directory
    directory=list()
    for z in range(20):
        directory.append(z)

    #first in list of classes is root file directory, list first items in root dir
    i=0
    directory[i]=navfolders.Navfolders(rootdir)
    print directory[i].currentdir, '\n'
    directory[i].listitems(4)



def select_item(btn):
    global i
    
    #create list of paths of items currently on screen
    selection_path=[]
    num_items=len(directory[i].currentitems)
    for x in range(num_items):
        selection_path.append(os.path.join(os.path.abspath(directory[i].currentdir),directory[i].currentitems[x]))
    
    if not btn>num_items:
        i+=1
        #os.system('clear')  #clear command line window
        
        # if selection is a directory, run Navfolders to list items in dir
        if os.path.isdir(selection_path[btn-1]):
            directory[i]=navfolders.Navfolders(selection_path[btn-1])
            print directory[i].currentdir, '\n'
            directory[i].listitems(4)
    
        # if selection is a file, play file
        elif os.path.isfile(selection_path[btn-1]):
            print  'this is file!!'
        


def navigate(direction):
    os.system('clear')
    print directory[i].currentdir, '\n'
    directory[i].navigatelist(direction)
    

def backdir():
    global i
    os.system('clear')
    i-=1
    print directory[i].currentdir, '\n'
    directory[i].listitems(4)

