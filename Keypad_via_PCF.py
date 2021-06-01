import smbus
import RPi.GPIO as GPIO
import time

bus = smbus.SMBus(1)
PCADDRESS = 0x20
#key pad
# cols
# 4 3 2 1

# 1 2 3 A       r   8
# 4 5 6 B       o   7
# 7 8 9 C       w   6
# * 0 # D       s   5
row_mask=   0b00001111
rows =      0b10000000

key_array = [['1'],['2'],['3'],['A']],\
            [['4'],['5'],['6'],['B']],\
            [['7'],['8'],['9'],['C']],\
            [['*'],['0'],['#'],['D']]

bus.write_byte(PCADDRESS, 0b11111111)  # put all pins as inputs => needs to be done once
#byte to set _______________87654321   cols=8765 rows=1234

PCF_INT = 18
LED_PIN = 23

while True:
    pressed = False
    col_mask = 0b00001111
    row_mask = 0b11110000
    while not pressed:
        row_bytes = 0b10000000
        for rows in range(4):#TODO: replace 4 by info from key_array
            col_bytes = 0b11110111
            for cols in range(4):#TODO: replace 4 by info from key_array
                col_bytes_write = col_bytes & col_mask #11110111 & 00001111 = 00000111
                #print("{0:08b}".format(col_bytes_write))
                row_bytes_write = row_bytes & row_mask #10000000 & 11110000 = 10000000
                #print("{0:08b}".format(row_bytes))

                write_bytes = row_bytes_write | col_bytes_write #0b10000000 | 0b00000111 = 0b10000111
                bus.write_byte(PCADDRESS,write_bytes)
                #here comes the row shift
                #print("{0:08b}".format(write_bytes))
                status=bus.read_byte(PCADDRESS)  & row_bytes
                #print("{0:08b}".format(status))
                if (status) == 0:
                    print(key_array[rows][cols])
                    pressed  =True
                    while pressed:
                        status = bus.read_byte(PCADDRESS) & row_bytes
                        # print("{0:08b}".format(status))
                        if (status) != 0: #wait untill button released
                            pressed = False
                col_bytes = col_bytes >> 1
            row_bytes = row_bytes >> 1











