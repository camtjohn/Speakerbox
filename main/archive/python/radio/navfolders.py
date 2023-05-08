import os

class Navfolders:
    def __init__(self, path):
        self.currentdir = path
        self.list_index=0
        
    # method: print list of items
    def listitems(self,listqty):
        self.listqty=listqty

        # list folders in current directory
        listfolders=[]
        filenames = sorted(os.listdir(self.currentdir))
        for filename in filenames:
            if os.path.isdir(os.path.join(os.path.abspath(self.currentdir),filename)):
                listfolders.append(filename)
        
        # list files in current directory
        listfiles=[]
        for filename in filenames:
            if os.path.isfile(os.path.join(os.path.abspath(self.currentdir),filename)):
                listfiles.append(filename)
        
        # merge all folders and files in directory into one list
        self.mergelist = listfolders + listfiles


        self.currentitems=[]
        self.numlist = len(self.mergelist)   #find total number of items in directory
        
        # print files/folders onto screen (listqty) items at a time
        for x in range(self.listqty):
            if self.list_index<self.numlist:
                self.currentitems.append(self.mergelist[self.list_index])
                print self.mergelist[self.list_index]
                self.list_index+=1
            else:
                print ' '
                self.currentitems.append(' ')
                self.list_index+=1
            
        self.list_index=self.list_index-self.listqty # reset counter to first item in list
   
        
    # method: navigate through list, listqty at a time
    def navigatelist(self,nav):
    
        if nav==6:  #navigate up
            if self.list_index+self.listqty>=self.numlist:
                self.listitems(self.listqty)
            else:
                self.list_index+=self.listqty
                self.listitems(self.listqty)  # call list method to print items to screen

        elif nav==5:  #navigate down
            self.list_index-=self.listqty
            if self.list_index < 0:
                self.list_index=0
            self.listitems(self.listqty)

        else:
            print 'your input got messed up'
