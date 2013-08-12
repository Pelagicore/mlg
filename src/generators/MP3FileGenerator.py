from abstract.AbstractFileGenerator import AbstractFileGenerator
import src.Sentences as s
import os, hashlib, subprocess, random, tempfile
from random import randint
from struct import pack
from distutils import spawn


class MP3FileGenerator (AbstractFileGenerator):
	lame_binary = spawn.find_executable("lame")
	id3v2_binary = spawn.find_executable("id3v2")
	convert_binary = spawn.find_executable("convert")

	def getFile(self, location = "/tmp/", properties = {}):
		print self.properties
		properties = dict(self.properties.items() + properties.items())
		print properties
		self.location = location
		if self._get_property("filename-naming-strategy", properties)\
		                      == "artist-title":
			properties["TPE1"] = self._get_property("TPE1",
			                                        properties)
			properties["TIT2"] = self._get_property("TIT2",
			                                        properties)
			filename = location + "/%s - %s.mp3" %\
			  (properties["TPE1"], properties["TIT2"])
		else:
			filename = self._get_filename(properties)
		if (self._generate_file(filename, properties)):
			return filename
		else:
			return None

	def getPropertyDescriptions(self):
		return {
		"filename-naming-strategy": (str, "Strategy to apply for "+\
		                     "naming files (artist-title / hash)"),
		"brokenness": (int, "Chance as a percentage that each tag "+\
		                    "is included in each file"),
		"TPE1": (str, "Performer of each track"),
		"TIT2": (str, "Title of each track"),
		"TALB": (str, "Album of each track"),
		"TCON": (int, "Genre of each track"),
		"TCOP": (str, "Copyright message of each track"),
		"COMM": (str, "Comment for each track"),
		"TYER": (int, "Year of each track"),
		"TRCK": (int, "Track number of each track"),
		"TPUB": (str, "Publisher of each track"),
		"TENC": (str, "Encoding software for each track")
		}


	def _generate_file(self, filename, properties):
		assert(self.lame_binary != None)
		assert(self.lame_binary != "")
		assert(filename != None)
		while os.path.exists(filename):
			filename = filename + "_"
		properties["album"] = self._get_property("TALB", properties)
		album = properties["album"]
		count = self._get_property("size_multiplier", properties)
		artf = self._generate_album_art(album)
		brokenness = self._get_property("brokenness", properties)
		fd = self.getRandomFile(count * 1048576)

		cmd = ("%s %s --scale 0.01" +\
		       " -r -b 320 -s 44 --ti \"%s\" - > \"%s\"") % \
			(self.lame_binary, fd.name, artf.name, filename)
		process = subprocess.call(cmd, shell=True)
		process = process + self._set_tags(properties, filename,
		              brokenness)

		fd.close()
		artf.close()
		return process == 0

	def _generate_album_art(self, text):
		fname = tempfile.NamedTemporaryFile(suffix=".jpg")
		cmd = ("%s -size 300x300 -fill white -background orange "+\
		"-gravity center label:\"%s\" %s") %\
		   (self.convert_binary, text, fname.name)
		process = subprocess.call(cmd, shell=True)
		return fname

	def _get_property(self, prop, properties):
		if properties is not None and prop in properties:
			return properties[prop]
		elif prop == "size_multiplier": return 15
		elif prop == "brokenness": return 0
		elif prop == "TPE1":
			if "artist" in properties: return properties["artist"]
			else: return s.getSentence()
		elif prop == "TIT2": return s.getSentence()
		elif prop == "TALB":
			if "album" in properties: return properties["album"]
			else: return s.getSentence()
		elif prop == "TCON": return randint(0,79)
		elif prop == "TCOP":
			return s.getSentence(randint(1,7))
		elif prop == "COMM":
			return s.getSentence(randint(1,20))
		elif prop == "TYER": return randint(1960, 2013)
		elif prop == "TRCK": return randint(1,15)
		elif prop == "TPUB": return s.getSentence()
		elif prop == "TENC": return s.getSentence()
		elif prop == "album": return s.getSentence()

	def _set_tags(self, properties, fname, brokenness):
		retvals = 0
		for fld in ["TPE1", "TIT2", "TALB", "TCON", "TCOP", "COMM",
		            "TYER", "TRCK", "TPUB", "TENC"]:
			if randint(1,100) > brokenness:
				fldval = self._get_property(fld, properties)
				retvals = retvals + \
				  subprocess.call("%s --%s \"%s\" \"%s\"" %
			            (self.id3v2_binary, fld, fldval, fname),
				    shell=True)
			else:
				print "NOT setting %s due to brokenness" % fld
		return retvals

	def _get_filename(self, properties):
		filename = None
		if properties is not None and "filename" in properties:
			filename = properties["filename"]
		else:
			filename = \
			  hashlib.md5(str(random.random())).hexdigest()+".mp3"
		assert(filename != None)
		return os.path.join(self.location, filename)









#Available ID3 tags to be applied to all files:
#	TPE1 TIT2 TALB TCON TCOP COMM TYER TRCK TPUB TENC
