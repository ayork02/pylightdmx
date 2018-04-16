import pylightdmx
from pylightdmx import rigs
from pylightdmx import fixtures

dmx = pylightdmx.DMXConnection("/dev/ttyUSB0")
r = rigs.Rig(dmx, "cultural_centre")

# r.g["Pars"].set_intensity(255)
# dmx.render()
