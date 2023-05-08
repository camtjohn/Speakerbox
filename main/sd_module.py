import os
import navfolders

class SD:
    def __init__(self):
        self.rootdir = '/home/pi/Music' #establish root directory
        self.directory = list()
        self.item_type = 'folder' #will immediately be overwritten once "select_item" is called
        
        self.start_sd()
        
    def start_sd(self):

        #establish a list of variables to be assigned to a class used for each file directory
        for z in range(20):
            self.directory.append(z)

        #first in list of classes is root file directory, list first items in root dir
        self.dir_lvl=0 #iterator through file directories (0 is root, 1 is next folder, etc.)
        self.directory[self.dir_lvl] = navfolders.Navfolders(self.rootdir)
        self.current_dir_class = self.directory[self.dir_lvl]
        self.current_dir_class.listitems(4)


    def select_item(self, btn):
        
        selection_path = [] #used to create list of url paths of items currently on screen
        self.directory_url=os.path.abspath(self.current_dir_class.currentdir) #url of current directory
        num_items=len(self.current_dir_class.currentitems)
        
        # create url by joining directory pathway with file name
        for x in range(num_items):
            selection_path.append(os.path.join(self.directory_url, self.current_dir_class.currentitems[x]))


        #If the button is empty, do nothing. Otherwise proceed
        if selection_path[btn-1] == self.directory_url + '/ ':
            self.item_type = ' '
        
        else:

            # if selection is a directory, increase directory level by one, run Navfolders to list items in dir
            if os.path.isdir(selection_path[btn-1]):
                self.dir_lvl += 1
                self.directory[self.dir_lvl] = navfolders.Navfolders(selection_path[btn-1])
                self.current_dir_class = self.directory[self.dir_lvl]
                self.current_dir_class.listitems(4)
                self.item_type='folder'
    
            # if selection is a file, return index of current song and list of files in folder
            elif os.path.isfile(selection_path[btn-1]):
                #calculate index of selected item in list of files (merged list index+item# on screen-number of folders)
                self.selected_song_index = self.current_dir_class.list_index + (btn-1) - len(self.current_dir_class.listfolders)
                self.files_in_folder = self.current_dir_class.listfiles
                self.item_type='file'


sd_class = SD()
