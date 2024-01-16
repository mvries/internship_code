#!/usr/bin/python3
"""
This script is used to find suitable primer sets for given sequences.

This script should be pointed to a directory with fasta files.

To run:
Python3 primer_finder.py fasta_dir output_dir
Author: Martijn de Vries (m97devries@gmail.com)
"""

#Classes:
class Fasta_File:
    """
    This class is used to represent a fasta file.

    '''
    Attributes:
        infile : Textfile
            Plain text file with DNA in fasta format.

    '''
    Methods:
        __init__:
            Function that initiates the CSV file object.
        read_file:
            Function to extract the contents of the fasta file.
    """
    def __init__(self, infile):
        """
        Function to initiate the Fasta_File object.
        """
        self.data = self.read_file(infile)

    def read_file(self, infile):
        """
        Function to read the contents of a fasta file.

        Input:
            infile : file
                plain text file with DNA seq in fasta format.

        Returns:
            contents : library
                library of {seq_ID : Seqeunce}
        """
        contents = {}
        id = None
        sequence = None

        with open(infile, 'r') as reader:
            for line in reader:
                if line[0] == ">":
                    id == line.strip(">")
                else:
