#!/usr/bin/env python
import sys
import os
import gzip
import getopt

###############################################################################

def generate_fasta(file, gz=False):
    seqid = None
    seq = ""
    release = ()
    with gzip.open(file, 'rt') if fz else open(file, 'r') as fd:
        for line in fd:
            if line[0] == '>':
                if seqid is None:
                    seqid = line.strip()
                else:
                    release = (seqid, seq)
                    seqid = line.strip()
                    seq = []
                    yield release
                #fi
            else:
                seq += line.strip()
            #fi
        #efor
        yield (seqid, seq)
    #ewith
#edef

###############################################################################
    
def generate_fastq(file, gz=False):
    seqid = None
    seq = None
    qual = None
    with gzip.open(file, 'rt') if gz else open(file, 'r') as fd:
        line = fd.readline()
        while line is not None:
            if len(line) == 0:
                line = fd.readline().strip()
                continue
            elif line[0] == '@':
                seqid = line.strip()[1:]
                seq   = fd.readline().strip()
                plus  = fd.readline()
                qual  = fd.readline().strip()
                
                line = fd.readline()
                yield (seqid, seq, qual)
                
            else:
                line = fd.readline()
            #fi
        #ewhile
    #ewith
#edef

###############################################################################

def fmt_fasta(seqid, seq, n=80):
    return '>%s\n%s' % (seqid, '\n'.join([seq[i:i+n] for i in range(0, len(seq), n)]))
#edef

def fmt_fastq(seqid, seq, qual='I'):
    seqlen = len(seq)
    return '@%s\n%s\n+\n%s' % (seqid, seq, qual if len(qual) == seqlen else (qual*seqlen))
#edef

###############################################################################
# PROCESS INPUTS
###############################################################################

options, args = getopt.getopt(sys.argv[1:], '', ['fqin','fqout','gzin','gzout'])
options = dict(options)
fqin = '--fqin' in options
fqout = '--fqout' in options
gzin = '--gzin' in options
gzout = '--gzout' in options

if len(args) != 3:
    print("Usage: %s [--fqin] [--fqout] [--gzin] [--gzout] <fasta/fastq file> <unaligned_table> <outfile>" % sys.argv[0])
    sys.exit(1)
#fi

file_in  = args[0]
unaln_in = args[1]
file_out = args[2]

###############################################################################
# START PROGRAM CODE
###############################################################################

fgen = generate_fastq(file_in, gz=gzin)
i = 0
with (gzip.open(file_out, 'wt') if gzout else open(file_out, 'w')) as fout:
    with open(unaln_in, 'r') as fin:
        for line in fin:
            line = line.strip().split()
            if line[1] != '*':
                continue
            #fi
            i += 1
            seqid = line[0]
            while True:
                seq = next(fgen)
                if seq[0].split()[0] == seqid:
                    outstr = fmt_fastq(seq[0], seq[1], (seq[2] if fqin else 'I')) if fqout else fmt_fasta(seq[0], seq[1])
                    fout.write(outstr + '\n')
                    break
                #fi
            #ewhile
        #efor
        print('Extracted %d unaligned sequences' % i)
    #ewith
#ewith