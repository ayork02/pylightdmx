from setuptools import setup

setup(name = "pylightdmx",
	version = "0.9.1",
	description = "Enttec DMX USB Pro Mk2 Lighting Controller",
	licence = "GPLV3",
	author = "ayork02",
	author_email = "ayork02@outlook.com",
	url = "http://github.com/ayork02/pylightdmx",
	install_requires = ["pyserial", "Pillow"],
	zip_safe = False
	)