import RPi.GPIO as GPIO
from time import sleep

class Cleaner:
    def __init__(self, en: int):
        self.en = en

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.en, GPIO.OUT)

    def enable(self):
        GPIO.output(self.en, GPIO.HIGH)
        print("Cleaner enabled")

    def disable(self):
        GPIO.output(self.en, GPIO.LOW)
        print("Cleaner disabled")

if __name__ == '__main__':
    cleaner = Cleaner(2)
    cleaner.enable()
    sleep(5)
    cleaner.disable()