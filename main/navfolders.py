import os

class Navfolders:
    def __init__(self, path):
        self.currentdir = path
        self.list_index=0
        
    # method: print list of items in current directory (first the folders then the files)
    def listitems(self,listqty):
        self.listqty=listqty

        filenames = sorted(os.listdir(self.currentdir))
        
        # list folders in current directory
        self.listfolders=[]
        for filename in filenames:
            if os.path.isdir(os.path.join(os.path.abspath(self.currentdir),filename)):
                self.listfolders.append(filename)
        
        # list files in current directory
        self.listfiles=[]
        for filename in filenames:
            if os.path.isfile(os.path.join(os.path.abspath(self.currentdir),filename)):
                self.listfiles.append(filename)
        
        # merge all folders and files in directory into one list
        self.mergelist = self.listfolders + self.listfiles


        self.currentitems=[]
        self.numlist = len(self.mergelist)   #find total number of items in directory
        
        # print files/folders onto screen (listqty) items at a time
        for x in range(self.listqty):
            if self.list_index < self.numlist:
                self.currentitems.append(self.mergelist[self.list_index])
                self.list_index += 1
            else:
                self.currentitems.append(' ')
                self.list_index += 1
            
        self.list_index=self.list_index-self.listqty # reset counter to first item in list
   
        
    # method: navigate through list of folders/files in director, listqty at a time
    def navigatelist(self,direction):
    
        if direction=='forward':
            if self.list_index + self.listqty < self.numlist: #if there are more items in the folder to show, show them
                self.list_index += self.listqty
                self.listitems(self.listqty)  # call list method to set current items to the variable called by gui

        elif direction=='backward':
            if self.list_index > 0:
                self.list_index -= self.listqty
                self.listitems(self.listqty)

