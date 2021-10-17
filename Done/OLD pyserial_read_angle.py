# Importing Libraries
import serial
import time

arduino = serial.Serial(port='/dev/tty.usbserial-1420', baudrate=115200, timeout=.1)


def getnumber(s):
    string = s.decode()
    n = int(string)
    return n


while True:
    num = input("Enter a number: ")  # Taking input from user
    arduino.write(bytes(num, 'utf-8'));
    time.sleep(0.05)
    sen = arduino.readline().decode()
    print(sen)
    if sen[0] == 'M':
        for x in range(180):
            for y in range(180):
                data = arduino.readline().decode()
                print(data)
                # data = arduino.readline()
                # num = getnumber(data)
                # print(num)
