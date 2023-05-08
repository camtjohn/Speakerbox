import pygame as pg
import sys
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

# set GPIO 7 as input. It's pulled up to stop false signals
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)

raw_input("Press enter now fool! but only when you're ready")

def run_game():
    pg.init()
    screen = pg.display.set_mode((1200,800))
    pg.display.set_caption("Aliens fuck!")
                
        
run_game()

print "Press button when ready to intitiate"


try:
    GPIO.wait_for_edge(7, GPIO.FALLING)
    print "Button pressed!!!"
    

except KeyboardInterrupt:
    GPIO.cleanup() #clean up GPIO on crtl+c exit
    
    
raw_input("Press enter to exit")

GPIO.cleanup() #clean up GPIO on normal exit