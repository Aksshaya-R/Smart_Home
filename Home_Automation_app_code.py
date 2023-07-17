
from socket import *
from time import ctime
import RPi.GPIO as GPIO
in1 = 6
in2 = 26
led_pin1 = 17
led_pin2 = 27
motor_pin = 5
moisture_pin = 22
# relay_pin = 6
motor_status = False
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin, GPIO.OUT)
x = GPIO.PWM(motor_pin,100)
x.start(0)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setwarnings(False)           #do not show any warnings
GPIO.setup(led_pin1,GPIO.OUT)           # initialize GPIO19 as an output.
p = GPIO.PWM(led_pin1,100)
GPIO.setup(led_pin2,GPIO.OUT)           # initialize GPIO19 as an output.
q = GPIO.PWM(led_pin2,100)
p.start(0)
q.start(0)
GPIO.setup(moisture_pin, GPIO.OUT)

HOST = ''
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST,PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
        print('Waiting for connection')
        tcpCliSock,addr = tcpSerSock.accept()
        print ('...connected from :', addr)
        try:
                while True:
                        data = ''
                        data = tcpCliSock.recv(100)
                        if not data:
                            break
                        data=data.decode("utf-8") 
                        if data=='B':
                            GPIO.output(in1, False)
                            print("OFF")
                        if data=='A':
                            GPIO.output(in1, True)
                            print("ON")
                        if data=='N':
                            GPIO.output(in2, False)
                            print("OFF")
                        if data=='O':
                            GPIO.output(in2, True)
                            print("ON")
                        #led 1
                        if data=='1':
                            p.ChangeDutyCycle(0) 
                            print("Level1")
                        if data=='2':
                            p.ChangeDutyCycle(50) 
                            print("Level2")
                        if data=='3':
                            p.ChangeDutyCycle(100) 
                            print("Level3")
                        if data=='D':
                            p.ChangeDutyCycle(0) 
                            print("LED turned on.")
                        if data=='C':
                            p.ChangeDutyCycle(100) 
                            print("LED turned OFF")
                        #led 2
                        if data=='6':
                            q.ChangeDutyCycle(100) 
                            print("Level1")
                        if data=='5':
                            q.ChangeDutyCycle(50) 
                            print("Level2")
                        if data=='4':
                            q.ChangeDutyCycle(0) 
                            print("Level3")
                        if data=='E':
                            q.ChangeDutyCycle(0)
                            print("LED turned on.")
                        if data=='F':
                            q.ChangeDutyCycle(100)
                            print("LED turned OFF")
                        #fan
                        if data=='7':
                            x.ChangeDutyCycle(65) 
                            print("Level1")
                        if data=='8':
                            x.ChangeDutyCycle(70) 
                            print("Level2")
                        if data=='9':
                            x.ChangeDutyCycle(100) 
                            print("Level3")
                        if data=='g':
                            x.ChangeDutyCycle(100)
                            print("ON.")
                        if data=='h':
                            x.ChangeDutyCycle(0)
                            print("fan OFF")
#                         soilmoisture sensor
                        if data=='Z':
                            GPIO.output(moisture_pin, False)
                            print("OFF")
                        if data=='Y':
                            GPIO.output(moisture_pin, True)
                            print("ON")
                            
                        

                               
        except KeyboardInterrupt:
                GPIO.cleanup()
tcpSerSock.close();