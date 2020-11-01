from sense_hat import SenseHat
import time
import vlc
# import os
import RPi.GPIO as GPIO

class halloween:
    def __init__(self):
        # PIN DEFINITIONS
        # GND - pin 39
        self.pin_beam = 26          # pin 37
        self.pin_doorbell = 19      # pin 35
        self.pin_dooropen = 13      # pin 33
        self.pin_other = 6          # pin 31
        self.pin_redeyes = 5        # pin 29
        self.redeyes_starttime = 0.0
        self.redeyes_state = 0

    def play_file(self, filename):
        print("Playing: " + filename)
        p = vlc.MediaPlayer(filename)
        p.play()
        # os.system("play " + filename)

    def handle_event(self, pin):
        if pin == self.pin_beam:
            self.sense.set_pixel(7,0,0,255,0)
            self.play_file("/home/pi/projects/halloween/Effects/owl.wav")
            self.redeyes_starttime = time.time()
        if pin == self.pin_doorbell:
            self.sense.set_pixel(7,1,0,255,0)
            self.play_file("/home/pi/projects/halloween/Effects/evillaff4.wav")
        if pin == self.pin_dooropen:
            self.sense.set_pixel(7,2,0,255,0)            
            self.play_file("/home/pi/projects/halloween/Effects/large_metal_rusty_door.mp3")
            self.play_file("/home/pi/projects/halloween/Effects/old_door_creaking.mp3") 
            # self.play_file("/home/pi/projects/halloween/Effects/cackle07.wav")
        if pin == self.pin_other:
            self.sense.set_pixel(7,3,0,255,0)
            self.play_file("/home/pi/projects/halloween/Effects/Raven_Sound_Clip.mp3")

    def check_gpio_toggle(self, pin, level_last, test_level=0):
        level = GPIO.input(pin)
        # print("Level: %d %d" % (level, level_last[0]))
        if level==test_level and level_last[0]!=test_level:
            print("GPIO %d event" % (pin))
            self.handle_event(pin)
        level_last[0] = level

    def blink_red_eyes(self):
        dt = time.time() - self.redeyes_starttime
        # print("dt: %d" % dt)
        if dt > 5.0 and dt < 20.0:
            if dt < 10.0:
                if self.redeyes_state:
                    self.redeyes_state = 0
                else:
                    self.redeyes_state = 1
                GPIO.output(self.pin_redeyes, self.redeyes_state)    # Toggle
            else:
                GPIO.output(self.pin_redeyes, 1)    # On
        else:
            GPIO.output(self.pin_redeyes, 0)    # Off

    def main(self):
        self.sense = SenseHat()
        # sense.show_message("Boo!!!", scroll_speed=0.05)

        # GPIO.setmode(GPIO.BOARD)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_doorbell, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_beam, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_dooropen, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_other, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.setup(self.pin_redeyes, GPIO.OUT)
        GPIO.output(self.pin_redeyes, 0)    # Off

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
        level_dooropen = [0]
        level_other = [0]

        while run:
            time.sleep(0.2)

            # Clear 
            for i in range(4):
                self.sense.set_pixel(7,i,0,0,0)

            self.check_gpio_toggle(self.pin_beam, level_beam)
            self.check_gpio_toggle(self.pin_doorbell, level_doorbell, test_level=1)
            self.check_gpio_toggle(self.pin_dooropen, level_dooropen)    
            self.check_gpio_toggle(self.pin_other, level_other)

            self.blink_red_eyes()

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
                        self.handle_event(self.pin_dooropen)
                    if event.direction == "left":
                        self.handle_event(self.pin_other)

        print("Quiting")
        self.sense.clear()
        # Free up resources and return I/O to inputs
        GPIO.cleanup()




h = halloween()
h.main()