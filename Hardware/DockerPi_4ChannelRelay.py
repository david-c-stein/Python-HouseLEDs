"""
DockerPi: 4 channel relay
    https://wiki.52pi.com/index.php/DockerPi_4_Channel_Relay_SKU:_EP-0099

    The following code is recommended to be executed using Python 3 and  install the smbus library:

    import time as t
    import smbus
    import sys

    DEVICE_BUS = 1
    DEVICE_ADDR = 0x10
    bus = smbus.SMBus(DEVICE_BUS)

    while True:
    try:
        for i in range(1,5):
        bus.write_byte_data(DEVICE_ADDR, i, 0xFF)
        t.sleep(1)
        bus.write_byte_data(DEVICE_ADDR, i, 0x00)
        t.sleep(1)
    except KeybaordInterrupt as e:
        print("Quit the Loop")
        sys.exit()

------------------------------------------------

Nice bit of info on smbus and i2c
https://www.abelectronics.co.uk/kb/article/1/i2c-part-2---enabling-i-c-on-the-raspberry-pi

sudo apt-get update
sudo apt-get install python-smbus python3-smbus python-dev python3-dev i2c-tools
sudo i2cdetect -y 1
"""

import smbus


class DocketPi_4_Channel_Relay(object):

    def __init__(self, address=0x10, bus=1):
        self.address = address
        self.bus = smbus.SMBus(bus)

    def on(self, relay):
        self.bus.write_byte_data(self.address, relay, 0xFF)

    def off(self, relay):
        self.bus.write_byte_data(self.address, relay, 0x00)

    def get_state(self, relay):
        return self.bus.read_byte_data(self.address, relay)


# test stuffs are here
if __name__ == '__main__':

    #--- basic DocketPi_4_Channel_Relay test ---
    relay = DocketPi_4_Channel_Relay(0x10, 1)

    for i in range(1,4):
        state = relay.getstate(1)
        print 'Relay: ' + str(i) + ' state: ' + str(state)

    for i in range(1,4):
        relay.on(i)
        
    for i in range(1,4):
        state = relay.getstate(1)
        print 'Relay: ' + str(i) + ' state: ' + str(state)

    for i in range(1,4):
        relay.off(i)

    for i in range(1,4):
        state = relay.getstate(1)
        print 'Relay: ' + str(i) + ' state: ' + str(state)




