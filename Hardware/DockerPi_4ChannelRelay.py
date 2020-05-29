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
"""

import smbus


class DocketPi_4_Channel_Relay(object):

    def __init__(self, address=0x10, bus=1):
	self.address = address
	self.bus = smbus.SMBus(bus)

    def relay_on(self, relay):
	self.bus.write_byte_data(self.address, relay, 0xFF)

    def relay_off(self, relay):
	self.bus.write_byte_data(self.address, relay, 0x00)

    def get_relay_state(self, relay):
	return self.bus.read_byte_data(self.address, relay)



