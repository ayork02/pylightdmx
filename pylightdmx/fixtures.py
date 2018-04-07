import json
import os
from PIL import ImageColor
import pylightdmx

class Fixture():
	def __init__(self, connection, brand, model, address):
		path = os.path.join(os.path.dirname(__file__), "rigs", "fixtures", brand, model + ".json")
		with open(path, 'r') as f:
			self.data = json.load(f)
		self.address = address
		self.link = connection
		self.name = self.data["shortName"]
		self.speed_offset = {}
		self.macro_offset = {}

	def __str__(self):
		return "{}, Address = {}".format(self.name, self.address)

	def rgb_control(self):
		self.r_offset = self.data["availableChannels"]["red"]["offset"]
		self.g_offset = self.data["availableChannels"]["green"]["offset"]
		self.b_offset = self.data["availableChannels"]["blue"]["offset"]

	def set_rgb(self, r, g, b):
		self.link.set_chan(self.address + self.r_offset, r)
		self.link.set_chan(self.address + self.g_offset, g)
		self.link.set_chan(self.address + self.b_offset, b)

	def set_colour(self, colour):
		r, g, b = ImageColor.getcolor(colour, "RGB")
		self.set_rgb(r, g, b)

	def intensity(self):
		self.intensity_offset = self.data["availableChannels"]["intensity"]["offset"]

	def set_intensity(self, val):
		if isinstance(val, int) == True:
			self.link.set_chan(self.address + self.intensity_offset, val)
		elif "%" in val:
			percent = float(val.strip('%'))/100
			val = int(percent * 255)
			self.link.set_chan(self.address + self.intensity_offset, val)

	def pan(self):
		self.pan_offset = self.data["availableChannels"]["pan"]["offset"]
		self.range = self.data["availableChannels"]["pan"]["range"]
		self.dmx_per_deg = 255/self.range

	def set_pan(self, val):
		if isinstance(val, int) == True:
			 self.link.set_chan(self.address + self.pan_offset, val)
		elif "*" in val:
			angle = float(val.strip("*"))
			val = int(angle * self.dmx_per_deg)
			self.link.set_chan(self.address + self.pan_offset, val) 

	def tilt(self):
		self.tilt_offset = self.data["availableChannels"]["tilt"]["offset"]
		self.range = self.data["availableChannels"]["tilt"]["range"]
		self.dmx_per_deg = 255/self.range

	def set_tilt(self, val):
		if isinstance(val, int) == True:
			 self.link.set_chan(self.address + self.tilt_offset, val)
		elif "*" in val:
			angle = float(val.strip("*"))
			val = int(angle * self.dmx_per_deg)
			self.link.set_chan(self.address + self.tilt_offset, val)

	def speed(self, name):
		self.speed_offset[name] = self.data["availableChannels"][name]["offset"]

	def set_speed(self, name, val):
		self.link.set_chan(self.address + self.speed_offset[name], val)

	def macros(self, name):
		self.macro_offset[name] = self.data["availableChannels"][name]["offset"]

	def set_macro(self, name, label):
		val = self.data["availableChannels"][name]["capabilities"][label]["startVal"] 
		self.link.set_chan(self.address + self.macro_offset[name], val)

	def config(self):
		for i in available_controls:
			for d in self.data["availableChannels"]:
				category = self.data["availableChannels"][d]["type"]
				if  category == i:
					if category == "macros" or category == "speed":
						getattr(self, i)(str(d))
					else:
						getattr(self, i)()
		if all(x in self.data["availableChannels"] for x in rgb_channels):
			self.rgb_control()
		
	def list_channels(self):
		return list(self.data["availableChannels"].keys())

available_controls = ["intensity", "pan", "tilt", "speed", "macros"]
rgb_channels = ["red", "green", "blue"]