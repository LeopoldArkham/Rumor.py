from random import random, randint

RUMOR_SIZE = 24
RUMOR_MAX_VALUE = (2 ** RUMOR_SIZE) - 1


class Person():
	"""
	Represents one user of the network
	"""

	# Rumor modifications modes:
	def incremental(self):
		return int(self._rumor + (randint(0, 1) - 0.5) * 2) % (RUMOR_MAX_VALUE + 1)

	def bitflip(self):
		return self._rumor ^ (1 << randint(0, RUMOR_SIZE))

	def noMod(self):
		return self._rumor

	# Rumor update modes:
	def stable(self, newRumor):
		if not self._rumor:
			self._rumor = newRumor

	def rewrite(self, newRumor):
		self._rumor = newRumor

	def mixture(self, newRumor):
		cur = bin(self._rumor)[2:]
		new = bin(newRumor)[2:]
		chose = lambda bit: bit if random() <= 0.9 else "10"[int(bit)]
		mix = [b1 if b1 is b2 else chose(b1) for b1, b2 in zip(cur, new)]
		self._rumor = int("".join(mix), 2)

	modificationModes = {"incremental" : incremental,
						 "bitflip"    : bitflip,
						 "none"       : noMod}
	
	updateModes = {"stable"  : stable,
				   "rewrite" : rewrite,
				   "mixture" : mixture}
	
	# Static
	modificationFunc = noMod
	modificationProbability = 0.1
	updateFunc = stable

	@staticmethod
	def setModificationMode(mode):
		if mode in Person.modificationModes.keys() :
			Person.modificationFunc = Person.modificationModes[mode]
		else:
			raise Exception()

	@staticmethod
	def setModificationProbability(prob):
		if 0.0 <= prob <= 1.0:
			Person.modificationProbability = prob
		else:
			raise Exception()

	@staticmethod
	def setUpdateMode(mode):
		if mode in Person.updateModes.keys() :
			Person.updateFunc = Person.updateModes[mode]
		else:
			raise Exception()

	# Instance methods
	def __init__(self, name, index):
		self._name = name
		self._rumor = None
		self._index = index

	def name(self):
		return self._name

	def index(self):
		return self._index

	def rumor(self):
		return self._rumor

	def setRumor(self, rumor):
		self._rumor = rumor

	def isInformed(self):
		return self._rumor is not None

	def tell(self, other):
		if random() <= Person.modificationProbability:
			rumor = self.modificationFunc()
		else:
			rumor = self._rumor

		other.updateFunc(rumor)