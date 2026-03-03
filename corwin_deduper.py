#!/usr/bin/env python

import argparse
import gzip
import numpy as np
import matplotlib.pyplot as plt
import re

# Define arguments that the user needs to input
def get_args():
    parser = argparse.ArgumentParser(description="This script produces a new SAM file without any PCR duplicates. This script assumes a sorted SAM file.")
    parser.add_argument("-f", "--file", help="The path to the sorted SAM file (str)", required=True, type=str)
    parser.add_argument("-o", "--outfile", help="The path to the outputed SAM file (str)", required=True, type=str)
    parser.add_argument("-u", "--umi", help="The path to the UMI file (str)", required=True, type=str)
    return parser.parse_args()
	
args = get_args()

# Functions
def determine_five_start(left_pos:int, strand:str, cigar:str) -> int:
    '''Given the 1-base leftmost starting position, strand, and cigar string, this function will output the 5 prime start of the read'''
    
    # Look for soft clipping on the positive strand
    if strand == "+":
        pattern = r"^[0-9]+S"
        result = re.match(pattern, cigar)

        if result:
            five_start = left_pos - int(result.group()[:-1])
        else:
            five_start = left_pos

    # Look for soft clipping on the negative strand
    elif strand == "-":
        cigar_separated = re.findall(r'\d+[a-zA-Z]?', cigar)
        five_start = left_pos

        for element in cigar_separated:
            if element[-1] in ("M", "D", "N"):
                number = int(element[:-1])
                five_start += number

        if cigar_separated[-1][-1] == "S":
            number = int(cigar_separated[-1][:-1])
            five_start += number

    return five_start

def read_info_tuple(read: str) -> tuple:
    '''Takes a read line, finds the chromosome #, strand, start of read, and UMI, and puts that information in a tuple'''
    read = read.strip('\n')

    # Get needed information from read
    fields = read.split("\t")
    umi = fields[0].split(':')[-1]
    flag = int(fields[1])
    chr = fields[2]
    left_pos = int(fields[3])
    cigar = fields[5]
    
    # Use flag to determine the strand
    if ((flag & 16) == 16):
        strand = "-"
    else:
        strand = "+"

    # Get the 5' start of the read
    five_start = determine_five_start(left_pos, strand, cigar)

    # Put all info in the tuple
    info_tuple = (chr, strand, five_start, umi)

    return info_tuple

# Create set of known UMIs
UMIs = set()
with open(args.umi, "r") as umi_fh:
    for line in umi_fh:
        line = line.strip('\n')
        UMIs.add(line)


# Read through SAM file and remove duplicates
have = set()
current_chr = "-1"
num_headers = 0
wrong_umis = set()
num_duplicates = 0
num_unique = 0
reads_per_chr = {}

with open(args.file, "r") as fh, open(args.outfile, "w") as out:
    for line in fh:
        line = line.strip('\n')

        # Write out all header lines
        if line.startswith("@"):
            out.write(f"{line}\n")
            num_headers += 1
        else:
            variables = read_info_tuple(line)

            # Check if UMI is in list of correct UMIs
            if variables[3] in UMIs:

                # Check if we are still on the same chromosome
                if variables[0] == current_chr:

                    # Check if our current variable tuple does not already exist (a sequence with the same information is already in our file)
                    # If new, write to outfile, if not increase duplicates count
                    if variables not in have:
                        have.add(variables)
                        out.write(f"{line}\n")
                        num_unique +=1
                        reads_per_chr[variables[0]] +=1
                    else:
                        num_duplicates += 1

                # Once on new chromosome, reset the set of existing sequences and write current sequence to outfile
                else:
                    current_chr = variables[0]
                    have.clear()
                    have.add(variables)
                    out.write(f"{line}\n")
                    num_unique +=1
                    reads_per_chr[variables[0]] = 1
            
            # If UMI does not exist in UMI file, add to set of incorrect UMIs
            else:
                wrong_umis.add(variables[3])

# Print out information about how many unique reads, duplicate reads, and wrong UMIs were in the file, among other useful information
print(f"Number of headers: {num_headers}")
print(f"Number of unique reads: {num_unique}")
print(f"Number of wrong UMIs: {len(wrong_umis)}")
print(f"Number of duplicate reads: {num_duplicates}\n")
print(f"Number of reads per chromosome:")
for chromosome in reads_per_chr:
    print(f"{chromosome}\t{reads_per_chr[chromosome]}")