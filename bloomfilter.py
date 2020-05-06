from pickle_hash import hash_code_hex

class BloomFilter(object):

	def __init__(self, size, hash_counts):
		self.size = size
		self.bloomfilter = [False] * size
		self.hash_counts = hash_counts

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
			pos.append(int(hash_code, 16) % self.size)
		return pos
