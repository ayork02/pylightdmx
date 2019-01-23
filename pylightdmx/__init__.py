# __init__.py

"""Basic lighting controller for Enttec DMX USB Pro Mk2"""

import serial
import sys
import time
import threading

start_val   = 0x7E
end_val     = 0xE7
output1     = 6
output2     = 202
api_key     = [0xC9, 0xA4, 0x03, 0xE4]
port_set	= [1, 1]

class DMXConnection:
	def __init__(self, port, output = 1):
		"""Creates a connection to the DMX device.

		Parameters
		----------
		port
			On Windows, port is the port number.
        	On Linux and macOS, port is the path to the serial device.
        output: int, optional(default=1)
			DMX output connected on DMX device.
			Unless output 2 is specified, configures to output 1.

        Examples
        --------
        >>> dmx = pylightdmx.DMXConnection(4) # Windows
        Opened COM4
        >>> dmx = pylightdmx.DMXConnection("/dev/ttyUSB0") # Linux
        Opened ttyUSB0
        """
		if isinstance(port, int): # Windows
			try:
				self.port = serial.Serial("COM%s" % (str(port)), 57600, timeout=1)
			except:
				print("Could not open device COM%s. Quitting application." % port)
				sys.exit(0)
		else: # Linux and macOS
			try:
				self.port = serial.Serial(port, 57600, timeout = 1)
			except:
				print("Could not open device %s. Quitting application." % port)
				sys.exit(0)
		print("Opened %s" % (self.port.portstr))
		self.dmx_frame = [0] * 513
		self.chan_list = {}
		if output == 2:
			self.label = output2
			packet = [
				start_val,
				13,
				4 & 0xFF,
				(4 >> 8) & 0xFF
				]
			packet += api_key
			packet.append(end_val)
			self.port.write(packet)
			time.sleep(1)
			packet2 = [
				start_val,
				147,
				2 & 0xFF,
				(2 >> 8) & 0xFF
				]
			packet2 += port_set
			packet2.append(end_val)
			self.port.write(packet2)
		else:
			self.label = output1
			


	
	def set_chan(self, chan, val, auto_render = False):
		"""Sets a channel level in local channel list.

		Parameters
		----------
		chan: int
			DMX channel to be assigned a value.
			Must be between 1 and 512.
		val: int
			Value to be assigned to DMX channel.
			Must be between 0 and 255.
		auto_render: bool, optional(default=False)
			If set to true, executes the set DMX channel.

		Raises
		------
		ValueError
			If the channel is not between 1 and 512.
		"""
		if not 1 <= chan <= 512:
			raise ValueError("Invalid channel specified: %s" % str(chan))
		val = max(0, min(val, 255)) # Restrict value
		self.chan_list[chan] = val
		if auto_render == True:
			self.render()

	def render(self, clear = True, newlist = True):
		"""Executes values in channel list.

		Parameters
		----------
		clear: bool, optional(default=True)
			If set to true, clears channels not in channel list.
		newlist: bool, optional(default=True)
			If set to true, clears the channel list.
		"""
		if clear == True: # Clear channels not specified
			for i in range(0, 512):  
				if i not in self.chan_list.keys():
					self.dmx_frame[i] = 0
		for i in self.chan_list.keys():
			self.dmx_frame[i] = self.chan_list[i]
		packet = [
				start_val,
				self.label,
				len(self.dmx_frame) & 0xFF,
				(len(self.dmx_frame) >> 8) & 0xFF
				]
		packet += self.dmx_frame
		packet.append(end_val)
		self.port.write(packet)
		self.chan_list.clear()
		if newlist == True:
			self.chan_list.clear()				

	def fade(self, chan, val, secs = 3):
		"""Fades a single channel to specified value.

		Parameters
		----------
		chan: int
			DMX channel to be assigned a value.
			Must be between 1 and 512.
		val: int
			Value to be assigned to DMX channel.
			Must be between 0 and 255.
		secs: int, optional(default=3)
			Determines how many seconds to fade the channel to specified value.
		"""
		val = max(0, min(val, 255))
		orig_val = self.dmx_frame[chan]
		if val > orig_val: # Fade in
			pause = 1 / ((val - orig_val) / secs / 3)
			while True:
				value = self.dmx_frame[chan] + 3
				self.set_chan(chan, value)
				self.render(clear = False, newlist = False)
				time.sleep(pause)
				if self.dmx_frame[chan] >= val - 3:
					self.set_chan(chan, val)
					self.render(clear = False, newlist = False)
					break
		elif val < orig_val: # Fade out
			pause = 1 / (abs(val - orig_val) / secs / 3)
			while True:
				value = self.dmx_frame[chan] - 3
				self.set_chan(chan, value)
				self.render(clear = False, newlist = False)
				time.sleep(pause)
				if self.dmx_frame[chan] <= val + 3:
					self.set_chan(chan, val)
					self.render(clear = False, newlist = False)
					break
		elif val == orig_val:
			pass
		
	def generate(self, secs = 3):
		"""Fades all channels in channel list.

		Parameters
		----------
		secs: int, optional(default=3)
			Determines how many seconds to fade the channels to the specified values.
		"""
		for i in range(0, 512):  
			if i not in self.chan_list.keys():
				self.dmx_frame[i] = 0
		for chan in set(self.chan_list.keys()):
			threading.Thread(target = self.fade, args = [chan, self.chan_list[chan], secs]).start()
		main_thread = threading.current_thread()
		for t in threading.enumerate():
			if t is main_thread:
				continue
			t.join()
		self.chan_list.clear()

	def DBO(self):
		"""Sets all channels to 0, causing a dead blackout"""
		self.dmx_frame = [0] * 513
		self.render() # Auto renders
		
	def close(self):
		"""Closes connection to DMX device."""
		self.port.close()