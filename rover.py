import RPi.GPIO as GPIO
from threading import Thread
from time import sleep
from motor import Motor
from cleaner import Cleaner
import socket
import numpy as np

class Rover(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.name = "odyssey"
        self.dc_right = 0
        self.dc_left = 0

        self.__MIN_BORDER = 85
        self.__MAX_BORDER = 100
        #self.right_motor = Motor(27, 10, 19, 100)
        #self.left_motor = Motor(24, 18, 26, 100)
    
    def __del__():
        GPIO.cleanup()

    #will wait until connections is established
    def init_server_socket(self, port:int):
        self.server_socket = socket.socket()
        self.server_socket.bind(('', port))
        
        print("Waiting for connection...")
        self.server_socket.listen(1)
        self.conn, self.addr = self.server_socket.accept()
        print("Connected: ", self.addr) 

    #message type is np.array 1x2 size [linear_speed, angular_speed]
    def get_message(self):
        message = np.frombuffer(self.conn.recv(88888), np.uint8)
        return message
    
    def close_connection(self):
        self.conn.close()

    def init_left_motor(self, en1:int, en2:int, enable:int):
        self.left_motor = Motor(en1, en2, enable, 100)
        self.left_motor.enable_motor()

    def init_right_motor(self, en1:int, en2:int, enable:int):
        self.right_motor = Motor(en1, en2, enable, 100)
        self.right_motor.enable_motor()
    
    def disable_motors(self):
        self.right_motor.disable_motor()
        self.left_motor.disable_motor()

    def to_string(self):
        print(self.name)
    
    def get_right_motors_pins(self):
        print("en_1 : " + str(self.en1_right) + " " + "en_2 : " + str(self.en2_right) + "  " + "enable : " + str(self.enable_right))


    def __less_than_min_border(self, dc_val:int = 0):
        if dc_val < self.__MIN_BORDER:
            return True
        else:
            return False

    def __more_than_max_border(self, dc_val:int = 0):
        if dc_val > self.__MAX_BORDER:
            return True
        else: 
            return False

    def stop_rover(self):
        self.__set_right_dc(0)
        self.__set_left_dc(0)

    def set_speed(self, linear_sp:int, angular_sp:int):
        if self.__less_than_min_border(linear_sp):
            linear_sp = self.__MIN_BORDER
            right_sp = linear_sp + angular_sp
            left_sp = linear_sp - angular_sp
        else: 
            right_sp = linear_sp + angular_sp
            left_sp = linear_sp - angular_sp

        if self.__more_than_max_border(right_sp):
            right_sp = self.__MAX_BORDER

        if self.__more_than_max_border(left_sp):
            left_sp = self.__MAX_BORDER

        self.__set_right_dc(right_sp)
        self.__set_left_dc(-left_sp)

    def __set_right_dc(self, new_right_dc:int):
        self.dc_right = new_right_dc

    def __set_left_dc(self, new_left_dc:int):
        self.dc_left = new_left_dc
    

    def run(self):
        while(1):
            self.right_motor.set_dc(self.dc_right)
            self.left_motor.set_dc(self.dc_left)

if __name__ == "__main__":
    rover = Rover()
    rover.to_string()
    rover.init_right_motor(27, 10, 19)
    rover.init_left_motor(24, 18, 26)
    rover.init_server_socket(9999)
    rover.setDaemon(True)
    rover.start()
    try:
        while(1):
            message = rover.get_message()
            if message.size == 0:
                print("Emty data received!")
            # get data from camera
            else:
                rover.set_speed(message[0], 0)
           # sleep(2)
           # rover.set_left_dc(85)
           # rover.set_right_dc(85)
           # sleep(2)
    except KeyboardInterrupt:
        rover.stop_rover()
        #rover.set_right_dc(0)
        rover.disable_motors()
        rover.close_connection()
    #rover.move_rover.set_rigrover.set_right_dc(50) ht_dc(50) right_motors_forward()
    #sleep(5)
    #rover.stop_motors()


