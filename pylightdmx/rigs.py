import json
import os
import pylightdmx
from pylightdmx import fixtures

class FixtureGroup:
	def __init__(self, connection, rig, name):
		"""Inititialises fixture group from rig definition.
		
		Parameters
		----------
		connection: obj
			The DMX connection opened by pylightdmx for the DMX device in use.
        rig: str
			The name of the rig.
			Must correspond to the file name of the JSON file.
		name: str
			The name of the fixture group.
			Must correspond to the fixture group name in the rig defintion.
		
        Examples
        --------
        >>> g = rigs.FixtureGroup(dmx, "example_rig", "Dimmers")
        """
		self.link = connection
		self.g = {}
		for fixture in rig.rig_data["groups"][name]:
			self.g[fixture] = fixtures.Fixture(connection, rig.rig_data["fixtures"][fixture]["brand"], rig.rig_data["fixtures"][fixture]["model"], rig.rig_data["fixtures"][fixture]["address"])
			self.g[fixture].config()
	
	def rgb_control(self):
		"""Initialises the ability to use the RGB channels of the fixture group."""
		for fixture in self.g.keys():
			self.g[fixture].rgb_control()
		
	def set_rgb(self, r, g, b):
		"""Sets the colour of the fixture group using RGB values.

		Parameters
		----------
		r: int
			Value to set the red value on the fixture group to.
		g: int
			Value to set the green value on the fixture group to.
		b: int
			Value to set the blue value on the fixture group to.

		Examples
		--------
		>>> LEDs = rigs.FixtureGroup(dmx, "example_rig", "LEDs")
		>>> LEDs.rgb_control()
		>>> LEDs.set_rgb(0, 128, 0)
		>>> dmx.render()
		"""
		for fixture in self.g.keys():
			self.g[fixture].set_rgb(r, g, b)
	
	def set_colour(self, colour):
		"""Sets the colour of the fixture group using the name of a colour.

		Parameters
		----------
		colour: str
			Colour to set the fixture group to.
		"""
		for fixture in self.g.keys():
			self.g[fixture].set_colour(colour)
		
	def intensity(self):
		"""Initialises the ability to use the intensity channel of the fixture group."""
		for fixture in self.g.keys():
			self.g[fixture].intensity()
		
	def set_intensity(self, val):
		"""Sets the intensity of the fixture group.

		Parameters
		----------
		val
			Value(int) or percentage(str) to set the intensity of the fixture group to.
		"""
		for fixture in self.g.keys():
			self.g[fixture].set_intensity(val)

	def strobe(self):
		"""Initialises the ability to use the strobe channel of the fixture group."""
		for fixture in self.g.keys():
			self.g[fixture].strobe()
		
	def set_strobe(self, val):
		"""Sets the strobe of the fixture group.

		Parameters
		----------
		val
			Value(int) or percentage(str) to set the strobe of the fixture group to.
		"""
		for fixture in self.g.keys():
			self.g[fixture].strobe(val)

	def focus(self):
		"""Initialises the ability to use the focus channel of the fixture group."""
		for fixture in self.g.keys():
			self.g[fixture].focus()
		
	def set_focus(self, val):
		"""Sets the focus of the fixture group.

		Parameters
		----------
		val
			Value(int) or percentage(str) to set the focus of the fixture group to.
		"""
		for fixture in self.g.keys():
			self.g[fixture].set_focus(val)
		
	def pan(self):
		"""Initialises the ability to use the pan channel of the fixture group."""
		for fixture in self.g.keys():
			self.g[fixture].pan()

	def set_pan(self, val):
		"""Sets the pan of the fixture group.

		Parameters
		----------
		val
			Value(int) or angle(str) to set the pan of the fixture group to.
		"""
		for fixture in self.g.keys():
			self.g[fixture].set_pan(val)
		
	def tilt(self):
		"""Initialises the ability to use the tilt channel of the fixture group."""
		for fixture in self.g.keys():
			self.g[fixture].tilt()
		
	def set_tilt(self, val):
		"""Sets the tilt of the fixture group.

		Parameters
		----------
		val
			Value(int) or angle(str) to set the tilt of the fixture group to.
		"""
		for fixture in self.g.keys():
			self.g[fixture].set_tilt(val)

	def speed(self, name):
		"""Initialises the ability to use a speed function of the fixture group.

		Parameters
		----------
		name: str
			Name of speed function to initialise.
		"""
		for fixture in self.g.keys():
			self.g[fixture].speed(name)

	def set_speed(self, name, val):
		"""Sets the value of a speed function of the fixture group.

		Parameters
		----------
		name: str
			Name of the speed function to assign a value to.
		val: int
			Value to set the speed function to.
		"""
		for fixture in self.g.keys():
			self.g[fixture].set_speed(name, val)

	def macros(self, name):
		"""Initialises the ability to use a macro channel of the fixture group.

		Parameters
		----------
		name: str
			Name of macro function to initialise.
		"""
		for fixture in self.g.keys():
			self.g[fixture].macros(name)

	def set_macro(self, name, label):
		"""Sets a macro of the fixture group.

		Parameters
		----------
		name: str
			Name of the macro to assign a value to.
		label: str
			Value to set the macro to. 
		"""
		for fixture in self.g.keys():
			self.g[fixture].set_macro(name, label)	

	def config(self):
		"""Initialises all available channels of the fixture group."""
		for fixture in self.g.keys():
			self.g[fixture].config()

		
class Rig:
	def __init__(self, connection, name):
		"""Opens JSON file containing rig definition and initialises all fixtures and fixture groups in the rig.

		Parameters
		----------
		connection: obj
			The DMX connection opened by pylightdmx for the DMX device in use.
        name: str
			The name of the rig.
			Must correspond to the file name of the JSON file.
		
        Examples
        --------
        >>> r = rigs.Rig(dmx, "example_rig")
        >>> r.f["LED1"].set_rgb(255, 0, 0) # Use of a fixture in rig
        >>> r.g["Dimmers"].set_intensity(255) # Use of a group in the rig
        """
		path = os.path.join(os.path.dirname(__file__), "rigs", name + ".json")
		with open(path, 'r') as f:
			self.rig_data = json.load(f)
		self.f = {}
		self.g = {}
		for name, d in self.rig_data["fixtures"].items():
			self.f[name] = fixtures.Fixture(connection, d["brand"], d["model"], d["address"])
			self.f[name].config()
		for name in self.rig_data["groups"]:
			self.g[name] = FixtureGroup(connection, self, name)
			self.g[name].config()