from setuptools import setup, find_packages

setup(name = "pylightdmx",
	version = "1.0.2",
	description = "Enttec DMX USB Pro Mk2 Lighting Controller",
	packages = find_packages(),
	license = "GPLV3",
	author = "ayork02",
	author_email = "ayork02@outlook.com",
	url = "https://github.com/ayork02/pylightdmx",
	classifiers = [
		"Development Status :: 3 - Alpha",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Programming Language :: Python :: 3"
	],
	install_requires = ["pyserial", "Pillow"]
	)