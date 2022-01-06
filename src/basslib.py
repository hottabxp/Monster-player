import ctypes
from ctypes import *


class Bass():

	def __init__(self):
		self._bass = ctypes.CDLL('./so/libbass.so')


	def init(self):
		init = self._bass.BASS_Init(-1,44100,0,0,0)
		return init


	def SetVolume(self, handle, volume):
		self._bass.BASS_ChannelSetAttribute.argtypes = [c_ulong, c_int, c_float]
		self._bass.BASS_ChannelSetAttribute(handle, 2, volume)

	def StreamCreateURL(self, url):
		self._bass.BASS_StreamCreateURL.restype = ctypes.c_ulong
		# self.url = ctypes.c_char_p(url.encode('ascii'))
		self._bass.BASS_StreamCreateURL.argtypes = [ctypes.c_char_p]
		# HSTREAM = ctypes.c_ulong(self._bass.BASS_StreamCreateURL(self.url,0,0,0,0))
		HSTREAM = self._bass.BASS_StreamCreateURL(url.encode(),0,0,0,0)
		return HSTREAM


	def Play(self, handle, restart):
		self._bass.BASS_ChannelPlay.argtypes = [c_ulong, c_bool]
		self._bass.BASS_ChannelPlay.restype = ctypes.c_bool
		status = self._bass.BASS_ChannelPlay(handle, restart)
		return status

	def Pause(self, handle):
		self._bass.BASS_ChannelPause.argtypes = [c_ulong]
		self._bass.BASS_ChannelPause.restype = c_bool
		status = self._bass.BASS_ChannelPause(handle)
		
		return status

	def Stop(self, handle):
		self._bass.BASS_ChannelStop.argtypes = [c_ulong]
		self._bass.BASS_ChannelStop.restype = c_bool
		status = self._bass.BASS_ChannelStop(handle)
		return status
		

	def Free(self):
		self._bass.BASS_Free.restype = ctypes.c_bool
		status = self._bass.BASS_Free()
		return status


	def GetVersion(self):
		self._bass.BASS_GetVersion.restype = ctypes.c_ulong
		bass_lib_version = self._bass.BASS_GetVersion()
		return bass_lib_version

	def ChannelGetTags(self, handle):
		self._bass.BASS_ChannelGetTags.argtypes = [c_ulong, c_ulong]
		self._bass.BASS_ChannelGetTags.restype = c_char_p
		_tags = self._bass.BASS_ChannelGetTags(handle, 5)

		if _tags:
			tags = _tags.decode()[13:-2]
		else:
			tags = 'Нет данных'


		return tags

# b= Bass()
# b.init()
# print(b)
# stream = b.StreamCreateURL('https://webhook.site/36841d65-3eac-4ebc-a8cb-0c2a0ce6f624')


# t = b.ChannelGetTags(stream)

# print(type(t))
# print(t)

# b.SetVolume(stream, 0.1)
# while True:
# 	b.Play(stream, False)

# v = b.GetVersion()
# print(type(v))
