import os
import vlc
import sd_module


class Player:
    def __init__(self):
        self.player_button_text = ' '
        self.volume_lvl = 70
        self.volume_label = str(self.volume_lvl)
        self.player_status = 0
        
    def play_selected_file(self):
    
        sd_class = sd_module.sd_class
        self.files_in_folder = sd_class.files_in_folder
        self.current_song_index = sd_class.selected_song_index
        self.player_button_text='Player View'

        if self.player_status == 0: #if player is stopped, play selected item
            self.new_playlist()
            self.vlc_play()
            self.player_status=1
            self.pause_button_text = 'Pause'
            
        elif self.player_status == 1: #else if the player is running, stop player, then play selected song
            self.new_playlist()
            self.player.stop()
            self.vlc_play()
            

    def new_playlist(self): #Create new playlist that starts from selected song
        sd_class = sd_module.sd_class
        self.playlist = []
        i = self.current_song_index
        self.current_song_title =self.files_in_folder[i]        
        num_files=len(self.files_in_folder)
        
        while i < num_files: #append song to playlist starting at current song until last in folder
            file_path = os.path.join(sd_class.directory_url, self.files_in_folder[i])
            self.playlist.append(file_path)
            i+=1

    def vlc_play(self):
        playlist = self.playlist
        self.player = vlc.MediaPlayer(playlist[0])
        self.player.audio_set_volume(self.volume_lvl)
        self.player.play()
            
        #self.player=vlc.MediaPlayer(playlist)
        #self.player.audio_set_volume(self.volume_lvl)
        #self.player.play()
    
    # Activate/deactivate player when press Play/Pause button and change button text
    def play_pause_song(self):
        
        if self.player_status == 0:
            self.player.play()
            self.player_status = 1
            self.pause_button_text = 'Pause'

        elif self.player_status == 1:
            self.player.pause()
            self.player_status = 0
            self.pause_button_text = 'Play'


    # Create playlist from current directory's list of files
    def next_song(self):
    
        if self.current_song_index < (len(self.files_in_folder)-1):    
            self.current_song_index += 1
            self.new_playlist()
            self.player.stop()
            self.vlc_play()
            
    def previous_song(self):
    
        if self.current_song_index > 0:
            self.current_song_index -=1
            self.new_playlist()
            self.player.stop()
            self.vlc_play()


    def volume_control(self, volume_direction):
        if volume_direction == 'up' and self.volume_lvl < 100:
            self.volume_lvl+=10
        if volume_direction == 'down' and self.volume_lvl > 0:
            self.volume_lvl-=10
            
        self.player.audio_set_volume(self.volume_lvl)
        self.volume_label = str(self.volume_lvl)
        
    def seek(self, btn):
        if btn == 1:
            self.player(rewind)
            


player_class=Player()


