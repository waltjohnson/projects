from sense_hat import SenseHat
from time import sleep
import vlc
# import os
import RPi.GPIO as GPIO

# PIN DEFINITIONS
# GND - pin 39
pin_beam = 26       # pin 37
pin_doorbell = 19   # pin 35
pin_other1 = 13     # pin 33
pin_other2 = 6      # pin 31

def play_file(filename):
    print("Playing: " + filename)
    p = vlc.MediaPlayer(filename)
    p.play()
    # os.system("play " + filename)

def handle_event(pin):
    if pin == pin_beam:
        play_file("/home/pi/projects/halloween/Effects/owl.wav")
    if pin == pin_doorbell:
        play_file("/home/pi/projects/halloween/Effects/evillaff4.wav")
    if pin == pin_other1:
        play_file("/home/pi/projects/halloween/Effects/cackle07.wav")
    if pin == pin_other2:
        play_file("/home/pi/projects/halloween/Effects/Raven_Sound_Clip.mp3")

def check_gpio_toggle(pin, level_last):
    level = GPIO.input(pin)
    # print("Level: %d %d" % (level, level_last[0]))
    if level==0 and level_last[0]==1:
        print("GPIO %d event" % (pin))
        handle_event(pin)
    level_last[0] = level

###############################################
# Main
sense = SenseHat()
# sense.show_message("Boo!!!", scroll_speed=0.05)

# GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_doorbell, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_beam, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_other1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_other2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# GPIO.setup(channel, GPIO.OUT)

X = [255, 0, 0]  # Red
# O = [255, 255, 255]  # White
O = [0, 0, 0]  # Off

question_mark = [
O, O, O, X, X, O, O, O,
O, O, X, O, O, X, O, O,
O, O, O, O, O, X, O, O,
O, O, O, O, X, O, O, O,
O, O, O, X, O, O, O, O,
O, O, O, X, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, X, O, O, O, O
]

isaac = [
O, X, X, X, X, X, X, O,
O, X, X, X, X, X, X, O,
O, O, O, X, X, O, O, O,
O, O, O, X, X, O, O, O,
O, O, O, X, X, O, O, O,
O, O, O, X, X, O, O, O,
O, X, X, X, X, X, X, O,
O, X, X, X, X, X, X, O
]

sense.set_pixels(isaac)

run = True
level_beam = [0]
level_doorbell = [0]
level_other1 = [0]
level_other2 = [0]

while run:
    sleep(0.2)

    check_gpio_toggle(pin_beam, level_beam)
    check_gpio_toggle(pin_doorbell, level_doorbell)
    check_gpio_toggle(pin_other1, level_other1)    
    check_gpio_toggle(pin_other2, level_other2)

    for event in sense.stick.get_events():
    # event = sense.stick.wait_for_event()
        print("The joystick was {} {}".format(event.action, event.direction))

        if (event.action == "pressed"):
            if event.direction == "middle":
                run = False

            if event.direction == "up":
                handle_event(pin_beam)
            if event.direction == "right":
                handle_event(pin_doorbell)
            if event.direction == "down":
                handle_event(pin_other1)
            if event.direction == "left":
                handle_event(pin_other2)

print("Quiting")
sense.clear()
# Free up resources and return I/O to inputs
GPIO.cleanup()
