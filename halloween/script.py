from sense_hat import SenseHat
from time import sleep
import vlc


def play_file(filename):
    print("Playing: " + filename)
    p = vlc.MediaPlayer(filename)
    p.play()



# Main
sense = SenseHat()

# sense.show_message("Boo!!!", scroll_speed=0.05)


run = True

while run:
    sleep(0.1)
    event = sense.stick.wait_for_event()
    # print("The joystick was {} {}".format(event.action, event.direction))
    sleep(0.1)

    if event.action == "pressed":
        # print("Button pressed!!!
        if event.direction == "up":
            print("Quiting")
            run = False

        if event.direction == "down":
            play_file("/home/pi/projects/halloween/Effects/evillaff4.wav")

        if event.direction == "left":
            play_file("/home/pi/projects/halloween/Effects/cackle07.wav")

        if event.direction == "right":
            play_file("/home/pi/projects/halloween/Effects/Raven_Sound_Clip.mp3")

        
