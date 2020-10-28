from sense_hat import SenseHat
from time import sleep
import vlc
# import os

def play_file(filename):
    print("Playing: " + filename)
    p = vlc.MediaPlayer(filename)
    p.play()
    # os.system("play " + filename)

# Main
sense = SenseHat()
# sense.show_message("Boo!!!", scroll_speed=0.05)

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

while run:
    sleep(0.1)
    event = sense.stick.wait_for_event()
    print("The joystick was {} {}".format(event.action, event.direction))

    if event.action == "pressed":
        if event.direction == "middle":
            run = False

        if event.direction == "up":
            play_file("/home/pi/projects/halloween/Effects/owl.wav")

        if event.direction == "down":
            play_file("/home/pi/projects/halloween/Effects/evillaff4.wav")

        if event.direction == "left":
            play_file("/home/pi/projects/halloween/Effects/cackle07.wav")

        if event.direction == "right":
            play_file("/home/pi/projects/halloween/Effects/Raven_Sound_Clip.mp3")

print("Quiting")
sense.clear()
