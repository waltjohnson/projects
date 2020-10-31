from sense_hat import SenseHat
from time import sleep
import vlc
# import os
import RPi.GPIO as GPIO

class halloween:
    def __init__(self):
        # PIN DEFINITIONS
        # GND - pin 39
        self.pin_beam = 26       # pin 37
        self.pin_doorbell = 19   # pin 35
        self.pin_other1 = 13     # pin 33
        self.pin_other2 = 6      # pin 31

    def play_file(self, filename):
        print("Playing: " + filename)
        p = vlc.MediaPlayer(filename)
        p.play()
        # os.system("play " + filename)

    def handle_event(self, pin):
        if pin == self.pin_beam:
            self.sense.set_pixel(7,0,0,255,0)
            self.play_file("/home/pi/projects/halloween/Effects/owl.wav")
        if pin == self.pin_doorbell:
            self.sense.set_pixel(7,1,0,255,0)
            self.play_file("/home/pi/projects/halloween/Effects/evillaff4.wav")
        if pin == self.pin_other1:
            self.sense.set_pixel(7,2,0,255,0)
            self.play_file("/home/pi/projects/halloween/Effects/cackle07.wav")
        if pin == self.pin_other2:
            self.sense.set_pixel(7,3,0,255,0)
            self.play_file("/home/pi/projects/halloween/Effects/Raven_Sound_Clip.mp3")

    def check_gpio_toggle(self, pin, level_last):
        level = GPIO.input(pin)
        # print("Level: %d %d" % (level, level_last[0]))
        if level==0 and level_last[0]==1:
            print("GPIO %d event" % (pin))
            self.handle_event(pin)
        level_last[0] = level

    def main(self):
        self.sense = SenseHat()
        # sense.show_message("Boo!!!", scroll_speed=0.05)

        # GPIO.setmode(GPIO.BOARD)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_doorbell, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_beam, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_other1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_other2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

        self.sense.set_pixels(isaac)

        run = True
        level_beam = [0]
        level_doorbell = [0]
        level_other1 = [0]
        level_other2 = [0]

        while run:
            sleep(0.25)

            # Clear 
            for i in range(4):
                self.sense.set_pixel(7,i,0,0,0)

            self.check_gpio_toggle(self.pin_beam, level_beam)
            self.check_gpio_toggle(self.pin_doorbell, level_doorbell)
            self.check_gpio_toggle(self.pin_other1, level_other1)    
            self.check_gpio_toggle(self.pin_other2, level_other2)

            for event in self.sense.stick.get_events():
            # event = self.sense.stick.wait_for_event() # blocks
                print("The joystick was {} {}".format(event.action, event.direction))

                if (event.action == "pressed"):
                    if event.direction == "middle":
                        run = False

                    if event.direction == "up":
                        self.handle_event(self.pin_beam)
                    if event.direction == "right":
                        self.handle_event(self.pin_doorbell)
                    if event.direction == "down":
                        self.handle_event(self.pin_other1)
                    if event.direction == "left":
                        self.handle_event(self.pin_other2)

        print("Quiting")
        self.sense.clear()
        # Free up resources and return I/O to inputs
        GPIO.cleanup()




h = halloween()
h.main()