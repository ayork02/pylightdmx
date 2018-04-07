import json
import os
import pylightdmx
from pylightdmx import fixtures

class Rig:
	def __init__(self, connection, name):
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


class FixtureGroup:
	def __init__(self, connection, rig, name):
		self.link = connection
		self.g = {}
		for fixture in rig.rig_data["groups"][name]:
			self.g[fixture] = fixtures.Fixture(connection, rig.rig_data["fixtures"][fixture]["brand"], rig.rig_data["fixtures"][fixture]["model"], rig.rig_data["fixtures"][fixture]["address"])
			self.g[fixture].config()
	
	def rgb_control(self):
		for fixture in self.g.keys():
			self.g[fixture].rgb_control()
		
	def set_rgb(self, r, g, b):
		for fixture in self.g.keys():
			self.g[fixture].set_rgb(r, g, b)
	
	def set_colour(self, colour):
		for fixture in self.g.keys():
			self.g[fixture].set_colour(colour)
		
	def intensity(self):
		for fixture in self.g.keys():
			self.g[fixture].intensity()
		
	def set_intensity(self, val):
		for fixture in self.g.keys():
			self.g[fixture].set_intensity(val)
		
	def pan(self):
		for fixture in self.g.keys():
			self.g[fixture].pan()

	def set_pan(self, val):
		for fixture in self.g.keys():
			self.g[fixture].set_pan(val)
		
	def tilt(self):
		for fixture in self.g.keys():
			self.g[fixture].tilt()
		
	def set_tilt(self, val):
		for fixture in self.g.keys():
			self.g[fixture].set_tilt(val)

	def speed(self, name):
		for fixture in self.g.keys():
			self.g[fixture].speed(name)

	def set_speed(self, name, val):
		for fixture in self.g.keys():
			self.g[fixture].set_speed(name, val)

	def macros(self, name):
		for fixture in self.g.keys():
			self.g[fixture].macros(name)

	def set_macro(self, name, label):
		for fixture in self.g.keys():
			self.g[fixture].set_macro(name, label)	

	def config(self):
		for fixture in self.g.keys():
			self.g[fixture].config()

		
