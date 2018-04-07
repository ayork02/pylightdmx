import serial
import sys
import time
import threading

start_val   = 0x7E
end_val     = 0xE7
output1      = 6
output2      = 202

class DMXConnection:
	def __init__(self, port):
		if isinstance(port, int) == True: # Windows
			try:
				self.port = serial.Serial('COM%s' % (str(port)), 57600, timeout=1)
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
		self.dmx_frame = [0] * 512
		self.chan_list = {}
	
	def set_chan(self, chan, val, auto_render = False):
		if not 1 <= chan <= 512:
			print("Invalid channel specified: %s' % str(chan)")
		val = max(0, min(val, 255)) # restrict value
		self.chan_list[chan] = val
		if auto_render == True:
			self.render()

	def render(self, output = 1, clear = True):
		if output == 2:
			label = output2
		else:
			label = output1
		if clear == True: # clear channels not specified
			for i in range(0, 512):  
				if i not in self.chan_list.keys():
					self.dmx_frame[i] = 0
		for i in self.chan_list.keys():
			self.dmx_frame[i] = self.chan_list[i]
		packet = [
				start_val,
				label,
				len(self.dmx_frame) & 0xFF,
				(len(self.dmx_frame) >> 8) & 0xFF
				]
		packet += self.dmx_frame
		packet.append(end_val)
		self.port.write(packet)
		self.chan_list.clear()		

	def fade(self, chan, val, secs = 3):
		val = max(0, min(val, 255))
		orig_val = self.dmx_frame[chan]
		if val > orig_val: # fade
			pause = 1 / ((val - orig_val) / secs / 3)
			while True:
				value = self.dmx_frame[chan] + 3
				self.set_chan(chan, value)
				self.render(clear = False)
				time.sleep(pause)
				print(self.dmx_frame[chan])
				if self.dmx_frame[chan] >= val - 3:
					self.set_chan(chan, val)
					self.render(clear = False)
					break
		elif val < orig_val: # fade out
			pause = 1 / (abs(val - orig_val) / secs / 3)
			while True:
				value = self.dmx_frame[chan] - 3
				self.set_chan(chan, value)
				time.sleep(pause)
				if self.dmx_frame[chan] <= val + 3:
					self.set_chan(chan, val)
					self.render(clear = False)
					break
		elif val == orig_val:
			pass
		
	def generate(self, secs = 3):
		for chan in self.chan_list.keys():
			threading.Thread(target = self.fade, args = [chan, self.chan_list[chan], secs]).start()
		main_thread = threading.current_thread()
		for t in threading.enumerate():
			if t is main_thread:
				continue
			t.join()
		self.chan_list.clear()

	def DBO(self):
		self.dmx_frame = [0] * 512
		self.render() # Auto Renders
		
	def close(self):
		self.port.close()