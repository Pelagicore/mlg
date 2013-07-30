import tempfile, random
from struct import pack

class AbstractFileGenerator:
	""" Abstract class fo file generators. These generators create files
	and supply the file names to the newly created file. """
	properties = {}

	def getFile(self, location = "/tmp/", properties = {}):
		""" Get a file from the generator. This file is disposable and
		can beused in any way.
		Parameters
		---------
		location : string
			A path indicating where the file should be created
		properties : dict
			A dictionary of generator-specific options, which can
			be bsed in any way the generator sees fit."""
		raise NotImplementedError

	def getRandomFile(self, filesize):
		""" Get a file pointer with contents generated using a PRNG.
		The contents of this file are affected by the seed parameter of
		the script
		Parameters
		----------
		filesize: integer
			Size of the generated file in bytes
		"""
		f = tempfile.NamedTemporaryFile(mode="wb")
		target = filesize / 8
		for x in range(0,target):
			f.write(pack("l", random.getrandbits(63)))
		f.flush()
		return f

	def setPersistantProperties(self, properties):
		""" Set a property dictionary which can be re-used in
		subsequent calls to this object. How to make use of this
		dictionary is up to the implementation, a recommendation is to
		merge this dictionary with the one supplied to getFile """
		self.properties = properties

	def getPropertyDescriptions(self):
		""" Get a string describing the available properties for this
		FileGenerator """
		raise NotImplementedError
