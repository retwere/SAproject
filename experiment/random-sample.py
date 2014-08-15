# Copyright 2014 Jake Fowler and Stephen Ra

"""Ouputs a random sample of N lines from stdin. Pass N as the command line 
argument."""


import random
import sys

def main(N):
    lines = sys.stdin.readlines()
    for i in random.sample(xrange(len(lines)), N):
        sys.stdout.write(lines[i])
    

if __name__ == '__main__':
    N = int(sys.argv[1])
    main(N)
