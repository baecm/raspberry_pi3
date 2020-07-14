import RPi.GPIO as GPIO


class LED:
    def __init__(self, pin=31):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.led_pin = pin

        GPIO.setup(self.led_pin, GPIO.OUT)
        self.off()

    def on(self):
        GPIO.output(self.led_pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.led_pin, GPIO.LOW)
