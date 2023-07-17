import serial
import RPi.GPIO as GPIO

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
pump_pin = 22
GPIO.setup(pump_pin, GPIO.OUT)

# Set up serial communication with Arduino
arduino_port = '/dev/ttyUSB0'  # Replace with the appropriate port
baud_rate = 9600
timeout = 5
ser = serial.Serial(arduino_port, baud_rate, timeout=timeout)
ser.reset_input_buffer()

# Define the threshold values for water intensity
dry_threshold = 500  # Adjust this value based on your sensor readings
wet_threshold = 800  # Adjust this value based on your sensor readings

while True:
    if ser.in_waiting > 0:
        val = ser.readline().decode('ascii').rstrip()
        moisture_value = int(val)

        # Determine the intensity of water pump based on soil moisture value
        if moisture_value < dry_threshold:
            # Water intensity is high
            GPIO.output(pump_pin, GPIO.HIGH)
            print("Watering with high intensity")
        elif moisture_value > wet_threshold:
            # Water intensity is low
            GPIO.output(pump_pin, GPIO.LOW)
            print("Watering with low intensity")
        else:
            # Soil moisture is within the desired range
            GPIO.output(pump_pin, GPIO.LOW)
            print("No watering required")

# Clean up GPIO on program exit
GPIO.cleanup()