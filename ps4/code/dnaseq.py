#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *
from kfasta import subsequences


### Utility classes ###

# Maps integer keys to a set of arbitrary values.

class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.data = dict()
        for pair in pairs:
            self.put(*pair)

    # Associates the value v with the key k.
    def put(self, k, v):
        self.data.setdefault(k, []).append(v)

    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        return self.data.get(k, [])
        

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)

def subsequenceHashes(seq, k):
    """
    Generates (hash, pos, subseq) pairs.
    """

    subseq = ''
    count = 0
    for char in seq:
        count += 1
        subseq += char
        if count is k:
            break
    hasher = RollingHash(subseq)

    pos = 0
    for char in seq:
        yield hasher.curhash, pos, subseq

        hasher.slide(subseq[0], char)
        subseq = subseq[1:] + char
        pos += 1
       


# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)

def intervalSubsequenceHashes(seq, k, m):
    """
    Generates (hash, pos, subseq) every m chars.
    """

    subseq = ''
    count = 0
    for char in seq:
        count += 1
        subseq += char
        if count is k:
            break
    hasher = RollingHash(subseq)

    pos = 0
    result = []
    for char in seq: 
        subseq += char
        pos += 1
        if pos % m is 0:
            hasher.slide(subseq[:m], subseq[-m:])
            subseq = subseq[m:]
            yield hasher.curhash, pos, subseq
        

# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).

def getExactSubmatches(a, b, k, m):
    """
    Generates (x, y) position of matches of nucleotides.
    """

    table = Multidict()
    for h, pos, seq in intervalSubsequenceHashes(a, k, m):
        table.put(h, (pos, seq))

    for h, y_pos, y_seq in subsequenceHashes(b, k):
        for x in table.get(h):
            # x_pos, y_pos
            yield x[0], y_pos


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0])
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
