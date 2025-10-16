# Define the problem

We are trying to code a way to remove PCR duplicates from our sam file. Duplictaes are reads that are on the same chromosome, have the same direction/strand, same 5' start of read (including soft clipping), and same UMI. We want to keep only the first instance of reads, and remove any subsequent duplcates.

# Psuedocode

- Use argparse for file inputs and outputs
- Read in UMI file create set of UMIs
- initiate set of tuples for duplicate factors (tuple with chromosome #, strand, start of read, UMI)
- Read in sam file and have output sam file open to write
- loop through input sam file line by line
    - if header line(^@), add to output sam file
    - get chromosome #(col 3), strand(col 2), start of read(col 4 and 6), and UMI(col 1) of current read and make it a tuple: MAKE FUNCTION
    - Check if current tuple is in set of tuples of existing reads
        - If yes it is a duplicate: do NOT add it to output sam file
        - If no, add tuple to set and write line to output sam file


## functions

```python
def read_info_tuple(read: str) -> tuple:
    '''Takes a read line, finds the chromosome #, strand, start of read, and UMI, and puts that information in a tuple'''
    return info_tuple
Input: "NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC	0	2	76814284	36	71M	*	0	0	TCCACCACAATCTTACCATCCTTCCTCCAGACCACATCGCGTTCTTTGTTCAACTCACAGCTCAAGTACAA	6AEEEEEEAEEAEEEEAAEEEEEEEEEAEEAEEAAEE<EEEEEEEEEAEEEEEEEAAEEAAAEAEEAEAE/	MD:Z:71	NH:i:1	HI:i:1	NM:i:0	SM:i:36	XQ:i:40	X2:i:0	XO:Z:UU"
Expected output: (2, '+', 76814284, CTGTTCAC)
```