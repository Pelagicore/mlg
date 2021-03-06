#!/usr/bin/env python
"""
This module is used to wrap the generator modules and supply them with
parameters set via the command line. This module serves as the main entry-point
to the file generator. Invoke it with --help to get a list of the available
configurations options
"""

import glob, importlib, argparse, itertools, hashlib, random, sys
import src.Sentences as Sentences
from src.DirectoryTreeGenerator import DirectoryTreeGenerator, FilePlacer
from random import randint

class FileGenerator:
	generatorModules = None
	currentGenerator = None

	def __init__(self):
		self.generatorModules = self.loadAvailableModules()

	def loadAvailableModules(self):
		""" Load all modules from the src/generators directory. """
		raw = glob.glob("src/generators/*.py")
		raw = filter(lambda x: not "__init__" in x, raw)
		raw = map(lambda x: x.replace("/", "."), raw)
		raw = map(lambda x: x.replace(".py", ""), raw)
		return raw

	def getGeneratorNames(self):
		return map(lambda x: x.split(".")[-1], self.generatorModules)

	def loadGenerator(self, generatorName):
		""" Assumes all generator modules contain a class with the same
		name as the file/module they are placed in
		Parameters
		----------
		generatorName : string
			A string with with a module and generator name (they
			must be the same)
		"""
		for g in self.generatorModules:
			if g.split(".")[-1] == generatorName:
				m = getattr(importlib.import_module(g),
					    g.split(".")[-1])
				self.currentGenerator = m
				return self.currentGenerator
		raise Exception("No such generator!")

	def generate(self, args):
		""" Generate files
		Parameters
		----------
		args: dict
			Contains key-value pairs generated by argparse
		"""
		if args.album_structure:
			self._generateAlbum(args)
		else:
			self._generateSingles(args)

	def _generateAlbum(self, args):
		dtg = DirectoryTreeGenerator()
		tree = dtg.generate(args.directory_depth, args.max_directories)
		fp = FilePlacer(tree)
		gen = fg.loadGenerator(args.generatorModule)()
		fp.generateAlbum(args, gen)

	def _generateSingles(self, args):
		dtg = DirectoryTreeGenerator()
		tree = dtg.generate(args.directory_depth, args.max_directories)
		gen = fg.loadGenerator(args.generatorModule)()
		fp = FilePlacer(tree)
		fp.generateSingles(args, gen)


def dump_settings(dest):
	""" Dump the arguments of the script to a file, so that this run can be
	reproduced """
	with open(dest, "w") as f:
		f.write(" ".join(sys.argv[:]))

def registerArguments(parser, fg):
	""" Register arguments for this script, this will query each module for
	their respective arguments and add these as sub-parameters triggered
	using the module name. General arguments common for all modules are
	also added by this function
	Parameters
	----------
	parser: argparser
		The argparser we should add the parameters to
	fg: A FileGenerator instance
		The FileGenerator we query for modules
	"""
	parser.add_argument("--max-albums-per-artist",type=int, default=4)
	parser.add_argument("--max-files-per-album",  type=int, default=15)
	parser.add_argument("--min-files-per-album",  type=int, default=5)
	parser.add_argument("--num-artists",          type=int, default=10)
	parser.add_argument("--album-structure", action="store_true")
	parser.add_argument("--destination-dir", type=str, default="/tmp/")
	parser.add_argument("--directory-depth", type=int, default=3)
	parser.add_argument("--max-directories", type=int, default=10)
	parser.add_argument("--num-files",       type=int, default=10)
	parser.add_argument("--size-multiplier", type=int, default=1)
	parser.add_argument("--random-seed",     type=int, default=None)
	parser.add_argument("--album-naming-strategy",type=str,
	            choices=["date", "music", "hash"], default="hash")
	parser.add_argument("--dump-settings", action="store_true")

	subparsers = parser.add_subparsers(dest="generatorModule")
	for g in fg.getGeneratorNames():
		p = subparsers.add_parser(g)
		fg.loadGenerator(g)
		descriptions = fg.currentGenerator().getPropertyDescriptions()
		for argName in descriptions:
			(t, desc) = descriptions[argName]
			p.add_argument("--%s" % argName, type=t,
				       help=desc, dest=argName)

if __name__ == "__main__":
	fg = FileGenerator()

	parser = argparse.ArgumentParser(
		description="Generate a multimedia library")
	registerArguments(parser, fg)

	args = parser.parse_args()

	# In order to reproduce results we may initialize the PRNG with a seed
	# of our choice. None here will mean a seed is picked for us
	random.seed(args.random_seed)

	if args.dump_settings:
		dump_settings("%s/%s" % (args.destination_dir, "args.txt"))

	fg.generate(args)
