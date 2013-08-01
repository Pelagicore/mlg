from src.generators import MP3FileGenerator
from src.generators import ImageFileGenerator
import src.Sentences as s
from src.DirectoryTreeGenerator import DirectoryTreeGenerator, FilePlacer
from pprint import pprint
from random import randint
import pytest, os, sys

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
		for album in range(0, randint(1,2)):
			album = s.getSentence()
			filename = "%s - %s.mp3" % (artist, album)
			gen.setPersistantProperties(
			   {"count":1,
			    "TPE1": artist,
			    "TALB": album,
			    "filename-naming-strategy": "artist-title"})
			numberOfTracks = randint(1,2)
			fp._placeAlbum(numberOfTracks, gen, album)
	fp._performActions("/tmp/generated_MP3s_remove")
	os.system("rm -rf /tmp/generated_MP3s_remove")

def _test_canPlacePhotos():
	tree = dtg.generate(5, 100)
	fp = FilePlacer(tree)
	gen = ImageFileGenerator.ImageFileGenerator()
	for artist in range(0,10):
		fp.placeFileGenerator(gen)
	fp.performActions("/tmp/generated/images/")

if __name__ == "__main__":
	print sys.argv
	pytest.main(args=["-s", os.path.abspath(__file__)])
