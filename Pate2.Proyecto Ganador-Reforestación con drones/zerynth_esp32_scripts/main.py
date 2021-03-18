################################################################################
# Zerynth UDP pinger
#
# Created by Zerynth Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

# import streams & socket
import streams
import socket

# import mcu to reset de micro controller
import mcu

# import our module created
import dispense

from espressif.esp32net import esp32wifi as wifi_driver

# import the wifi interface
from wireless import wifi

# the wifi module needs a networking driver to be loaded
# in order to control the board hardware.
# FOR THIS EXAMPLE TO WORK, A NETWORK DRIVER MUST BE SELECTED BELOW

# uncomment the following line to use the CC3000 driver (Particle Core or CC3000 Wifi shields)
# from texas.cc3000 import cc3000 as wifi_driver

# uncomment the following line to use the BCM43362 driver (Particle Photon)
# from broadcom.bcm43362 import bcm43362 as wifi_driver

streams.serial()

# init the wifi driver!
# The driver automatically registers itself to the wifi interface
# with the correct configuration for the selected board
wifi_driver.auto_init()

# IP and port of Tello
tello_address = ('192.168.10.1', 8889)
# IP and port of local computer
# local_address = ('', 9000)

# use the wifi interface to link to the Access Point
# change network name, security and password as needed
print("Establishing Link...")
try:
    # connect to tello wifi
    print("Connecting to Wifi")
    wifi.link("TELLO-AB0980", wifi.WIFI_OPEN)
    print("Establishing socket")
    sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
    print("Binding local address?")
    sock.bind(9999) # extracted from udp pinger
except Exception as e:
    print("ooops, something wrong while linking :(\n", e)
    while True:
        sleep(1000) # wait 1 second
        mcu.reset() # restarting o reseting mcu
        

# Send the message to Tello and allow for a delay in seconds
def send(message, delay):
    # Try to send the message otherwise print the exception
    try:
        sock.sendto(message, tello_address)
        print("Sending message: " + message)
    except Exception as e:
        print("Error sending: " + str(e))

    # Delay for a user-defined period of time
    sleep(delay*1000)


def receive():
    # Continuously loop and listen for incoming messages
    while True:
        # Try to receive the message otherwise print the exception
        try:
            response, ip_address = sock.recvfrom(128)
            print("Received message: " + response)
        except Exception as e:
            # If there's an error close the socket and break out of the loop
            # sock.close()
            print("Error receiving: " + str(e))
            break


# launch it!
thread(receive)

# in the main thread we listen for incoming udp packets
while True:
    # we deposit 1 seed every corner
    try:

        # Each leg of the box will be 100 cm. Tello uses cm units by default.
        box_leg_distance = 50

        # Yaw 90 degrees
        yaw_angle = 90

        # Yaw clockwise (right)
        yaw_direction = "cw"

        # Put Tello into command mode
        send("command", 3)
        # Send the takeoff command
        send("takeoff", 5)

        # Fly forward
        send("forward " + str(box_leg_distance), 4)
        dispense.seeds(1) # this should be blocking
    

        # Yaw right
        send("cw " + str(yaw_angle), 3)
        # Fly forward
        send("forward " + str(box_leg_distance), 4)
        dispense.seeds(1) # this should be blocking

        # Yaw right
        send("cw " + str(yaw_angle), 3)
        # Fly forward
        send("forward " + str(box_leg_distance), 4)
        dispense.seeds(1) # this should be blocking

        # Yaw right
        send("cw " + str(yaw_angle), 3)
        # Fly forward
        send("forward " + str(box_leg_distance), 4)
        dispense.seeds(1) # this should be blocking

        # Yaw right
        send("cw " + str(yaw_angle), 3)

        # Land
        send("land", 5)

        # Print message
        print("Mission completed successfully!")
        sock.close()
        sleep(5000) # wait 5 seconds
        mcu.reset() # restart esp32

    except Exception as e:
        print(e)
        sleep(5000) # wait 5 seconds
        mcu.reset() # restart esp32
# uplink this script to more than one board and check
