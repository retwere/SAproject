"""create the experimental dataset files
usage: python experiment/create-datasets.py <N> <r> <outdir> <input>
where N = number of samples in each file, r = number of files to create,
outdir = directory to store the output files, and input = (preprocessed) 
dataset"""

from subprocess import check_output
import sys

if __name__ == '__main__':
    samples = int(sys.argv[1]) # Number of samples
    repeat = int(sys.argv[2]) # number of times to repeat the sampling
    outdir = sys.argv[3] # directory for output (leave off the trailing /)
    inputfile = sys.argv[4] # file for the input
    
    for i in range(repeat):
        check_output("python experiment/random-sample.py {0} < {1} > {2}/{3} ".format(samples,inputfile,outdir,i),shell=True)
