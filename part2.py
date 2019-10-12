import copy
import sys


class Linear_Hash():
    '''
    Hash table object for duplicate elimination.
    Contains buckets and uses Dynamic Hashing. Splitting occurs when a bucket overflows.

    N = Initial number of buckets in hash table,
    B = Size of each bucket
    '''

    def __init__(self, N, B):
        self.initial_bucket_size = N
        self.buckets = [[] for _ in range(N)]
        self.max_bucket_size = B
        self.split_ptr = 0
        self.level = 1
    
    def _hash(self, key, i):
        '''
        Returns value of i rightmost bits of key
        '''
        return key % (1 << i)
    
    def _split(self):
        '''
        Splits the bucket pointed by split pointer
        '''
        temp_bucket = copy.deepcopy(self.buckets[self.split_ptr])
        self.buckets[self.split_ptr] = []
        self.buckets.append([])

        for key in temp_bucket:
            self.buckets[self._hash(key, self.level + 1)].append(key)
        
        self.split_ptr += 1
        if self.split_ptr == self.initial_bucket_size:
            self.initial_bucket_size <<= 1
            self.split_ptr = 0
            self.level += 1

    def insert(self, value):
        '''
        Inserts value into hashtable
        '''
        hash_value = self._hash(value, self.level)
        if hash_value < self.split_ptr:
            hash_value = self._hash(value, self.level + 1)
        
        if value in self.buckets[hash_value]:
            return False
        else:
            self.buckets[hash_value].append(value)
            if len(self.buckets[hash_value]) > self.max_bucket_size:
                self._split()
            return True
    
    def _show(self):
        '''
        Prints entire hashtable
        '''
        print("total buckets =", len(self.buckets))
        for i, bucket in enumerate(self.buckets):
            print(i, bucket)


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: python3 part2.py <filepath>')
        exit(1)
    
    filepath = sys.argv[1]
    records = open(filepath).readlines()
    records = [int(x.split()[0]) for x in records]

    H = Linear_Hash(2, 2)
    for record in records:
        if H.insert(record):
            print(record)
        # H._show
