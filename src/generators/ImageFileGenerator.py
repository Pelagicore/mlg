from src.generators.abstract.AbstractFileGenerator import AbstractFileGenerator
import os, binascii, subprocess, random, hashlib, tempfile
import src.Sentences as s
from random import randint, choice
from distutils import spawn


class ImageFileGenerator (AbstractFileGenerator):
	convert_binary = spawn.find_executable("convert")
	exiftool_binary = spawn.find_executable("exiftool")

	def getFile(self, location = "/tmp/", properties = {}):
		properties = dict(self.properties.items() + properties.items())
		self.location = location
		fd = self._get_file(properties)
		res = self._generate_file(fd.name, properties)
		os.system("rm %s_original" % fd.name)
		if res:
			return fd.name
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
#		elif prop == "Artist": return s.getFullName()
		elif prop == "Author": return s.getFullName()
		elif prop == "Date" or \
		     prop == "CreationTime" or \
		     prop == "-PNG:CreationTime":
			y = randint(1900, 2014)
			m = randint(1,12)
			d = randint(1,28)
			return "%04d:%02d:%02d" % (y,m,d)
		elif prop == "-EXIF:DateTimeOriginal":
			y = randint(1900, 2014)
			m = randint(1,12)
			d = randint(1,28)
			H = randint(0,24)
			M = randint(0,59)
			S = randint(0,59)
			return "%04d:%02d:%02d %02d:%02d:%02d" % (y,m,d,H,M,S)
		elif prop == "Make": return s.getSurname()
		elif prop == "Model": return s.getSurname()
		elif prop == "Copyright": return s.getSentence(5)
		elif prop == "WhiteBalance": return choice(["AUTO", "MANUAL"])
		elif prop == "Fnumber": return "%d" % choice([0.7, 0.8, 1.0,
		              2.2, 1.4, 1.7, 2, 2.4, 2.8, 3.3, 4, 4.8, 5.6])
		elif prop == "Flash": return choice(["ON", "OFF"])
		elif prop == "FocalLength": return randint(1,1000)
		elif prop == "ExposureTime": return randint(1,1000)
		elif prop == "ISO": return choice([100,200,300,400,500,600])
		elif prop == "Description": return s.getSentence(20)
#		elif prop == "Creator": return s.getFullName()
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
		for fld in ["Title",
		            "Author",
#		            "Artist",
		            "Date",
		            "Make",
		            "Model",
		            "Copyright",
		            "WhiteBalance",
		            "Fnumber",
		            "Flash",
		            "FocalLength",
		            "ExposureTime",
		            "ISO",
		            "Description",
#		            "Creator",
		            "Comment",
		            "City",
		            "State",
		            "Address",
		            "Country",
		            "CreationTime",
			    "-PNG:CreationTime",
			    "-EXIF:DateTimeOriginal",
		            "GPSLongitude",
		            "GPSLatitude"]:
			if randint(1,100) > brokenness:
				fldval = self._get_property(fld, properties)
				cmd = cmd + " -%s=\"%s\" " %\
			            (fld, fldval)
			else:
				print "NOT setting %s due to brokenness" % fld

		cmd = cmd + fname
		retval = subprocess.call(cmd, shell=True)
		return retval

	def _get_file(self, properties):
		fd = None
		if properties is not None and "filename" in properties:
			fd = open(properties["filename"])
		else:
			extension = self._get_property("extension", properties)
			fd = tempfile.NamedTemporaryFile(suffix="."+extension,
		          delete=False)
			fd.close()
		assert(fd != None)
		return fd

