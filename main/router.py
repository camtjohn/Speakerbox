

def filter_calls(btn):
    global current_window
    global playlist
    global player
    global player_status
    global volume_lvl
    global current_song
    global pause_button_text
    global player_button_text
    
    global label_text
    label_text=str(btn)
    
    if current_window=='main':
        if btn==1:
            current_window=window_mode[1]
            sdcalls.start_sd()
            window1.new_sdwindow()

        elif btn==2:
            bluecalls.blue_out()
        elif btn==3: print('\n FM radio')
        elif btn==4: print('\n Aux selected')
        elif btn==5: os.system('sudo reboot now')
        elif btn==6: os.system('sudo shutdown now')
        elif btn==7:
            current_window=window_mode[2]
            window1.close_sdwindow()
            window1.new_playerwindow()


    elif current_window=='sd_navfolder':
        
        if btn>0 and btn<=4:
            player, player_status, player_button_text, playlist, current_song, current_window = item_selection(btn, current_window, player, player_status, player_button_text, volume_lvl)

        elif btn==5 or btn==6:
            sdcalls.navigate(btn)
            window1.close_sdwindow()
            window1.new_sdwindow()

        elif btn==7:
            if sdcalls.dir_lvl>0:
                sdcalls.backdir()
                window1.close_sdwindow()
                window1.new_sdwindow()
            else:
                current_window=window_mode[0]
                window1.close_sdwindow()
                
        elif btn==8:
            current_window=window_mode[2]
            window1.close_sdwindow()
            window1.new_playerwindow()
                
    
    elif current_window=='player':
        
        if btn==1: #if paused=play and turn button to 'pause', if playing=pause and turn button to 'play'
            if player_status==0:
                player.play()
                player_status = 1
                pause_button_text='Pause'
                window1.close_playerwindow()
                window1.new_playerwindow()
            elif player_status==1:
                player.pause()
                player_status=0
                pause_button_text='Play'
                window1.close_playerwindow()
                window1.new_playerwindow()

        elif btn==2:
            print('unassigned')
            
        elif btn==3: #play next song in playlist, ensure 'play' button is appropriately named
            current_song, player = next_song(player, playlist, volume_lvl, current_song)
            if player_status==0:
                player_status=1
                pause_button_text='Pause'
                window1.close_playerwindow()
                window1.new_playerwindow()
                
        elif btn==4: #play previous song in playlist, ensure 'play' button is appropriately named
            current_song, player = previous_song(player, playlist, volume_lvl, current_song)
            if player_status==0:
                player_status=1
                pause_button_text='Pause'
                window1.close_playerwindow()
                window1.new_playerwindow()

        elif btn==5:
            volume_lvl=volume_control('up', volume_lvl)

        elif btn==6:
            volume_lvl=volume_control('down', volume_lvl)

        elif btn==7:
            current_window=window_mode[1]
            window1.close_playerwindow()
            window1.new_sdwindow()
