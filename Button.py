import RPi.GPIO as GPIO


class Button:
    def __init__(self, pin=29):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.button_pin = pin

        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
        GPIO.add_event_detect(self.button_pin, GPIO.BOTH)
