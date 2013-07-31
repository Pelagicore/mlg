from src.generators.abstract.AbstractFileGenerator import AbstractFileGenerator
import os, binascii, subprocess, random, hashlib
import src.Sentences as s
from random import randint, choice
from distutils import spawn


class ImageFileGenerator (AbstractFileGenerator):
	convert_binary = spawn.find_executable("convert")
	exiftool_binary = spawn.find_executable("exiftool")

	def getFile(self, location = "/tmp/", properties = {}):
		properties = dict(self.properties.items() + properties.items())
		self.location = location
		filename = self._get_filename(properties)
		if (self._generate_file(filename, properties)):
			return filename
		else:
			return None

	def getPropertyDescriptions(self):
		return {"extension": (str, "Only generate files with the"+\
		                           " supplied extension"),
		        "brokenness": (str, "Percentage of missing properties"),
		       }

	def _generate_file(self, filename, properties):
		size = self._get_property("WxH", properties)
		cmd = ("%s -size %s -seed %s +noise Random "+\
		"-gravity center label:\"%s\" \"%s\"") %\
		   (self.convert_binary, size, randint(0,99999),
		    "HELLOWORLD", filename)
		process = subprocess.call(cmd, shell=True)
		self._set_tags(properties, filename, 0)
		return process == 0

	def _get_property(self, prop, properties):
		if properties is not None and prop in properties:
			return properties[prop]
		elif prop == "size_multiplier": return 1
		elif prop == "WxH":
			ct = self._get_property("size_multiplier", properties)
			return "%sx%s" % (randint(10,80) * ct,
			                  randint(10,80) * ct)
		elif prop == "extension":
			return choice(["jpg", "png", "gif", "tiff"])
		elif prop == "Title": return s.getSentence()
		elif prop == "Artist": return s.getFullName()
		elif prop == "Author": return s.getFullName()
		elif prop == "DateCreated":
			y = randint(1900, 2014)
			m = randint(1,12)
			d = randint(1,28)
			return "%04d:%02d:%02d" % (y,m,d)
		elif prop == "Make": return s.getSurname()
		elif prop == "Model": return s.getSurname()
		elif prop == "Copyright": return s.getSentence(5)
		elif prop == "WhiteBalance": return choice(["AUTO", "MANUAL"])
		elif prop == "Fnumber": return "1/%d" % randint(2,800)
		elif prop == "Flash": return choice(["ON", "OFF"])
		elif prop == "FocalLength": return randint(1,1000)
		elif prop == "ExposureTime": return randint(1,1000)
		elif prop == "ISO": return choice([100,200,300,400,500,600])
		elif prop == "Description": return s.getSentence(20)
		elif prop == "Creator": return s.getFullName()
		elif prop == "Comment": return s.getSentence(20)
		elif prop == "City": return s.getFirstName()+"stown"
		elif prop == "State": return s.getFirstName()+"ina"
		elif prop == "Address": return s.getFirstName()+" road"
		elif prop == "Country": return s.getFirstName()+"ina"
		elif prop == "GPSLongitude": return randint(1,360)
		elif prop == "GPSLatitude": return randint(1,360)
		else: return ""

	def _set_tags(self, properties, fname, brokenness):
		retval = 0
		cmd = "%s " % self.exiftool_binary
		for fld in ["Title", "Author", "Artist", "DateCreated", "Make", 
		"Model", "Copyright", "WhiteBalance", "Fnumber", "Flash",
		"FocalLength", "ExposureTime", "ISO", "Description", "Creator",
		"Comment", "City", "State", "Address", "Country",
		"GPSLongitude", "GPSLatitude"]:
			if randint(1,100) > brokenness:
				fldval = self._get_property(fld, properties)
				cmd = cmd + " -%s=\"%s\" " %\
			            (fld, fldval)
			else:
				print "NOT setting %s due to brokenness" % fld

		cmd = cmd + fname
		retval = subprocess.call(cmd, shell=True)
		return retval

	def _get_filename(self, properties):
		filename = None
		if properties is not None and "filename" in properties:
			filename = properties["filename"]
		else:
			extension = self._get_property("extension", properties)
			filename = \
			 hashlib.md5(str(random.random())).hexdigest() +\
			 ".%s" % extension
		assert(filename != None)
		return os.path.join(self.location, filename)

