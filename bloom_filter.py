import math

from pickle_hash import hash_code_hex

class BloomFilter(object):

	def __init__(self, n, p):
		self.p = p # Probability of desired false positive rate
		self.n = n # number of expected keys to be stored
		self.m = self.__get_bit_array_size()
		self.bloomfilter = [False] * self.m
		self.hash_counts = self.__get_hash_counts()

	def add(self, key):
		for p in self.get_pos(key):
			self.bloomfilter[p] = True

	def is_member(self, key):
		return False if False in [self.bloomfilter[p] for p in self.get_pos(key)] else True

	def get_pos(self, key):
		hash_code = key
		pos = []
		for i in range(self.hash_counts):
			hash_code = hash_code_hex(hash_code.encode())
			pos.append(int(hash_code, 16) % self.m)
		return pos

	def __get_bit_array_size(self):
		return int(-(self.n * math.log(self.p))/(math.log(2)**2))

	def __get_hash_counts(self):
		return int((self.m/self.n) * math.log(2))
