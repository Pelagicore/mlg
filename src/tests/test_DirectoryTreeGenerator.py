from ..generators import MP3FileGenerator
from ..generators import ImageFileGenerator
import src.Sentences as s
from src.DirectoryTreeGenerator import DirectoryTreeGenerator, FilePlacer
from pprint import pprint
from random import randint

def setup_module(module):
	module.dtg = DirectoryTreeGenerator()

def test_canGenerate():
	num_dirs = 10
	max_depth = 3
	tree = dtg.generate(max_depth, num_dirs)
	assert (len(tree) == num_dirs)
	assert (max(map(len, tree)) <= max_depth)

def _test_canHandleExtremeDepth():
	num_dirs = 8e4
	max_depth = 8e4
	tree = dtg.generate(max_depth, num_dirs)
	assert (len(tree) == num_dirs)
	assert (max(map(len, tree)) <= max_depth)

def _test_canHandleExtremeWidth():
	num_dirs = 8e4
	max_depth = 3
	tree = dtg.generate(max_depth, num_dirs)
	assert (len(tree) == num_dirs)
	assert (max(map(len, tree)) <= max_depth)

def test_canPlaceMp3s():
	tree = dtg.generate(5, 100)
	fp = FilePlacer(tree)
	gen = MP3FileGenerator.MP3FileGenerator()
	for artist in range(0,1):
		artist = s.getSentence()
		for album in range(1, randint(1,4)):
			album = s.getSentence()
			filename = "%s - %s" % (artist, album)
			gen.setPersistantProperties({"count":1,
			                            "TPE1": artist,
			                            "TALB": album,
			                            "naming": "realistic"})
			numberOfTracks = randint(5,15)
			fp.placeAlbum(numberOfTracks, gen, album)
	fp.performActions("/tmp/generated/mp3/")

def _test_canPlacePhotos():
	tree = dtg.generate(5, 100)
	fp = FilePlacer(tree)
	gen = ImageFileGenerator.ImageFileGenerator()
	for artist in range(0,10):
		fp.placeFileGenerator(gen)
	fp.performActions("/tmp/generated/images/")
