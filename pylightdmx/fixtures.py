# fixtures.py

"""Adds fixture definitions for use with pylightdmx"""

import json
import os
from PIL import ImageColor
import pylightdmx

available_controls = ["intensity", "pan", "tilt", "speed", "macros", "focus", "strobe"]
rgb_channels = ["red", "green", "blue"]

class Fixture():
	def __init__(self, connection, brand, model, address):
		"""Opens JSON file containing fixture definition.

		Parameters
		----------
		connection: obj
			The DMX connection opened by pylightdmx for the DMX device in use.
        brand: str
			The brand of the fixture.
			Must correspond to the directory the JSON file is located in.
		model: str
			The name of the fixture.
			Must correspond to the file name of the JSON file.
		address: int
			The first DMX channel to be used by the fixture.

        Examples
        --------
        >>> LED = fixtures.Fixture(dmx, "Generic", "RGB", 1)
        """
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
		"""Initialises the ability to use the RGB channels of the fixture."""
		self.r_offset = self.data["availableChannels"]["red"]["offset"]
		self.g_offset = self.data["availableChannels"]["green"]["offset"]
		self.b_offset = self.data["availableChannels"]["blue"]["offset"]

	def set_rgb(self, r, g, b):
		"""Sets the colour of the fixture using RGB values.

		Parameters
		----------
		r: int
			Value to set the red value on the fixture to.
		g: int
			Value to set the green value on the fixture to.
		b: int
			Value to set the blue value on the fixture to.

		Examples
		--------
		>>> LED = fixtures.Fixture(dmx, "Generic", "RGB", 1)
		>>> LED.rgb_control()
		>>> LED.set_rgb(0, 128, 0)
		>>> dmx.render()
		"""
		self.link.set_chan(self.address + self.r_offset, r)
		self.link.set_chan(self.address + self.g_offset, g)
		self.link.set_chan(self.address + self.b_offset, b)

	def set_colour(self, colour):
		"""Sets the colour of the fixture using the name of a colour.

		Parameters
		----------
		colour: str
			Colour to set the fixture to.
		"""
		r, g, b = ImageColor.getcolor(colour, "RGB")
		self.set_rgb(r, g, b)

	def intensity(self):
		"""Initialises the ability to use the intensity channel of the fixture."""
		self.intensity_offset = self.data["availableChannels"]["intensity"]["offset"]

	def set_intensity(self, val):
		"""Sets the intensity of the fixture.

		Parameters
		----------
		val
			Value(int) or percentage(str) to set the intensity of the fixture to.

		Examples
		--------
		>>> Par = fixtures.Fixture(dmx, "Generic", "Dimmer", 1)
		>>> Par.intensity()
		>>> Par.set_intensity(255)
		>>> dmx.render()
		>>> Par.set_intensity("75%")
		>>> dmx.render()
		"""
		if isinstance(val, int):
			self.link.set_chan(self.address + self.intensity_offset, val)
		elif "%" in val:
			percent = float(val.strip('%'))/100
			val = int(percent * 255)
			self.link.set_chan(self.address + self.intensity_offset, val)

	def strobe(self):
		"""Initialises the ability to use the strobe channel of the fixture."""
		self.strobe_offset = self.data["availableChannels"]["strobe"]["offset"]

	def set_strobe(self, val):
		"""Sets the strobe of the fixture.

		Parameters
		----------
		val
			Value(int) or percentage(str) to set the strobe of the fixture to.
		"""
		if isinstance(val, int):
			self.link.set_chan(self.address + self.strobe_offset, val)
		elif "%" in val:
			percent = float(val.strip('%'))/100
			val = int(percent * 255)
			self.link.set_chan(self.address + self.strobe_offset, val)

	def focus(self):
		"""Initialises the ability to use the focus channel of the fixture."""
		self.focus_offset = self.data["availableChannels"]["focus"]["offset"]

	def set_focus(self, val):
		"""Sets the focus of the fixture.

		Parameters
		----------
		val
			Value(int) or percentage(str) to set the focus of the fixture to.
		"""
		if isinstance(val, int):
			self.link.set_chan(self.address + self.focus_offset, val)
		elif "%" in val:
			percent = float(val.strip('%'))/100
			val = int(percent * 255)
			self.link.set_chan(self.address + self.focus_offset, val)

	def pan(self):
		"""Initialises the ability to use the pan channel of the fixture."""
		self.pan_offset = self.data["availableChannels"]["pan"]["offset"]
		self.range = self.data["availableChannels"]["pan"]["range"]
		self.dmx_per_deg = 255/self.range

	def set_pan(self, val):
		"""Sets the pan of the fixture.

		Parameters
		----------
		val
			Value(int) or angle(str) to set the pan of the fixture to.

		Examples
		--------
		>>> MH = fixtures.Fixture(dmx, "iSolution", "iMove-8s", 1)
		>>> MH.pan()
		>>> MH.set_pan(255)
		>>> dmx.render()
		>>> MH.set_pan("180*")
		>>> dmx.render()
		"""
		if isinstance(val, int):
			 self.link.set_chan(self.address + self.pan_offset, val)
		elif "*" in val:
			angle = float(val.strip("*"))
			val = int(angle * self.dmx_per_deg)
			self.link.set_chan(self.address + self.pan_offset, val) 

	def tilt(self):
		"""Initialises the ability to use the tilt channel of the fixture."""
		self.tilt_offset = self.data["availableChannels"]["tilt"]["offset"]
		self.range = self.data["availableChannels"]["tilt"]["range"]
		self.dmx_per_deg = 255/self.range

	def set_tilt(self, val):
		"""Sets the tilt of the fixture.

		Parameters
		----------
		val
			Value(int) or angle(str) to set the tilt of the fixture to.
		"""
		if isinstance(val, int):
			 self.link.set_chan(self.address + self.tilt_offset, val)
		elif "*" in val:
			angle = float(val.strip("*"))
			val = int(angle * self.dmx_per_deg)
			self.link.set_chan(self.address + self.tilt_offset, val)

	def speed(self, name):
		"""Initialises the ability to use a speed function of the fixture.

		Parameters
		----------
		name: str
			Name of speed function to initialise.

		Examples
		--------
		>>> MH = fixtures.Fixture(dmx, "Rave", "Mini_Spot_Moving_Head", 1)
		>>> MH.speed("Pan/Tilt Speed")
		"""
		self.speed_offset[name] = self.data["availableChannels"][name]["offset"]

	def set_speed(self, name, val):
		"""Sets the value of a speed function of the fixture.

		Parameters
		----------
		name: str
			Name of the speed function to assign a value to.
		val: int
			Value to set the speed function to.

		Examples
		--------
		>>> MH = fixtures.Fixture(dmx, "Rave", "Mini_Spot_Moving_Head", 1)
		>>> MH.speed("Pan/Tilt Speed")
		>>> MH.set_speed("Pan/Tilt Speed", 255)
		>>> dmx.render()
		"""
		self.link.set_chan(self.address + self.speed_offset[name], val)

	def macros(self, name):
		"""Initialises the ability to use a macro channel of the fixture.

		Parameters
		----------
		name: str
			Name of macro function to initialise.

		Examples
		--------
		>>> MH = fixtures.Fixture(dmx, "Rave", "Mini_Spot_Moving_Head", 1)
		>>> MH.macros("Colour Macros")
		"""
		self.macro_offset[name] = self.data["availableChannels"][name]["offset"]

	def set_macro(self, name, label):
		"""Sets a macro of the fixture.

		Parameters
		----------
		name: str
			Name of the macro to assign a value to.
		label: str
			Value to set the macro to. 

		Examples
		--------
		>>> MH = fixtures.Fixture(dmx, "Rave", "Mini_Spot_Moving_Head", 1)
		>>> MH.macros("Colour Macros")
		>>> MH.set_macro("Colour Macros", "magenta")
		>>> dmx.render()
		"""
		val = self.data["availableChannels"][name]["capabilities"][label]["startVal"] 
		self.link.set_chan(self.address + self.macro_offset[name], val)

	def config(self):
		"""Initialises all available channels of the fixture."""
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
		"""Lists available channels of the fixture."""
		return list(self.data["availableChannels"].keys())