import pytest, os, stat
import MP3FileGenerator

def setup_module(module):
	module.generator = MP3FileGenerator.MP3FileGenerator()
	module.getFileResult = generator.getFile()

def teardown_module(module):
	os.remove(module.getFileResult)

def test_fileExists():
	if (not os.path.exists(getFileResult)):
		pytest.fail("Path returned by getFile does not exist!")

def test_fileHasCorrectAccessRights():
	st = os.stat(getFileResult)
	if not stat.S_ISREG (st.st_mode):
		pytest.fail ("Returned file is not a regular file!")
	if st.st_uid  != os.getuid():
		pytest.fail ("Current user does not own generated file!")
	if st.st_size < 10:
		pytest.fail ("File smaller than 10 bytes, something wrong?")

def test_canSupplyFilename():
	gen = MP3FileGenerator.MP3FileGenerator()
	assert (gen.getFile("/tmp/", {"filename": "myFile.mp3"}) ==
	        "/tmp/myFile.mp3")
	os.remove("/tmp/myFile.mp3")

def test_canCreateSmallFile():
	gen = MP3FileGenerator.MP3FileGenerator()
	fn = gen.getFile("/tmp/", {"count": 1})
	if os.stat(fn).st_size > 2e6:
		pytest.fail("Generated file looks suspiciously large")
	os.remove(fn)

def test_canCreateLargeFile():
	gen = MP3FileGenerator.MP3FileGenerator()
	fn = gen.getFile("/tmp/", {"count": 15})
	if os.stat(fn).st_size < 2e6:
		pytest.fail("Generated file looks suspiciously small")
	os.remove(fn)
