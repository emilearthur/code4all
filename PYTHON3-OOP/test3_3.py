import abc 

class AudioFile:
	def __init__(self, filename):
		if not filename.endswith(self.ext):
			raise Exception("Invalid file format")

		self.filename = filename

class MP3File(AudioFile):
	ext = "mp3"

	def play(self):
		print("Playing {} as mp3".format(self.filename))

class WavFile(AudioFile):
	ext = "wav"

	def play(self):
		print("Playing {} as wav".format(self.filename))

class OggFile(AudioFile):
	ext = "ogg"

	def play(self):
		print("Playing {} as ogg".format(self.filename))

class FlacFIle:
	def __init__(self, filename):
		if not filename.endswith(".flac"):
			raise Exception("Invalid file format")

		self.file = filename

	def play(self):
		print("playing {} as flac".format(self.filename))




class OddContainer:
	def __contains__(self,x):
		if not isinstance(x, int) or not x%2:
			return False 
		return True


class MediaLoader(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def play(self):
		pass

	@abc.abstractproperty
	def ext(self):
		pass 

	@classmethod
	def __subclasshook__(cls, C):
		if cls is MediaLoader:
			attrs = set(dir(C))
			if set(cls.__abstractmethods__) <= attrs:
				return True 

		return NotImplemented
			