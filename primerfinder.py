#!/usr/bin/python3
"""
This script is used to find suitable primer sets for given sequences.

This script should be pointed to a directory with fasta files.

To run:
Python3 primer_finder.py fasta_dir output_dir primer_length
Author: Martijn de Vries (m97devries@gmail.com)
"""

#import statements:
from sys import argv

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
            Function that initiates the Fasta_File file object.
        read_file:
            Function to extract the contents of the fasta file.
        get_kmers:
            Function that extracts kmers from the sequences in the file.
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
                library of {seq_ID : Sequence}
        """
        contents = {}

        with open(infile, 'r') as reader:
            for line in reader:
                if line[0] == ">":
                    id = line.strip(">\n")
                else:
                    contents[id] = line.strip("\n")

        return contents

    def get_kmers(self, kmerlength):
        """
        Function to retrieve kmers from the sequences.

        Input:
            contents : dict
                library of {seq_ID : Sequence}

            length : int
                integer representing desired kmer lenght.

        Returns:
            kmers : dict
                dict of {seq_id : {Position : Kmer}}

        """
        kmers = {}

        for key in self.data.keys():
            kmers[key] = {}
            position = 0
            sequence = self.data[key]
            while position < len(sequence) - kmerlength:
                kmer = sequence[position:(position + kmerlength) + 1]
                kmers[key][position] = kmer
                position += 1

        return kmers

class Kmer_Dict:
    """
    This class represents a dictionary of kmers.

    '''
    Attributes:
        kmer_dict: dictionary
            dict of {seq_id : {Position : Kmer}}

    '''
    Methods:
        __init__:
            Function that initiates the Kmer_Dict object.
    """
    def __init__(self, input_dict):
        """
        Function to initiate the Kmer_Dict object.
        """
        self.dict = input_dict

    def find_primer_regions(self):
        """
        Function used to find interesting regions for primers.
        """
        for key1 in self.dict.keys():
            kmers = self.dict[key1]
            for key2 in list(kmers.keys()):
                kmer = kmers[key2]
                good_region = True

                GC_count = 0
                Previous_base = ""
                Repetitions = 0

                for base in kmer:
                    if base == "G" or base == "C":
                        GC_count += 1
                    if base == Previous_base:
                        Repetitions += 1
                        if Repetitions == 4:
                            good_region = False
                            break
                    Previous_base = base

                GC_content = (GC_count) / len(kmer)
                if GC_content <=  0.55  and GC_content  >= 0.50:
                    pass
                else:
                    good_region = False

                if good_region == False:
                    del self.dict[key1][key2]

    def get_primers(self):
        """
        Function to retrieve viable primers.
        """
        primer_dict = {'forward':{}, 'reverse' : {}}


        for key1 in self.dict.keys():
            kmers = self.dict[key1]
            for key2 in list(kmers.keys()):
                kmer = kmers[key2]

                if kmer[-1] == "G" or kmer[-1] == "C":
                    primer_dict['forward'][key2] = kmer
                if kmer[0] == "G" or kmer[0] == "C":
                    revcomp = ""
                    for base in kmer[::-1]:
                        if base == "A":
                            revcomp += "T"
                        if base == "T":
                            revcomp += "A"
                        if base == "C":
                            revcomp += "G"
                        if base == "G":
                            revcomp += "C"
                    primer_dict['reverse'][key2] = revcomp

        return primer_dict

    def check_primers(self, primer_dict):
        """
        Function that does a last quality check of the retrieved primers:

        Note, this needs to use the primer dict of the previous function.
        """

        #First we check for dimers:
        for key1 in self.dict.keys():
            kmers = self.dict[key1]
            for key2 in list(kmers.keys()):
                kmer = kmers[key2]
                good_primer = True

                sub_kmers = []
                rev_kmers = []

                position = 0
                while position < (len(kmer) - 2):
                    sub_kmer = kmer[position:(position + 3)]
                    position += 1
                    sub_kmers.append(sub_kmer)

                position = 0
                while position < (len(kmer) - 2):
                    sub_kmer = kmer[::-1][position:(position + 3)]
                    position += 1
                    rev_kmers.append(sub_kmer)

                for kmer1 in sub_kmers:
                    for kmer2 in rev_kmers:
                        position = 0
                        complementary_bases = 0


                        while position < 3:
                            base1 = kmer1[position]
                            base2 = kmer2[position]
                            complement = self.is_complement(base1, base2)
                            if complement == True:
                                complementary_bases += 1
                            position += 1

                        if complementary_bases == 3:
                            good_primer = False
                        else:
                            continue

                    if good_primer == False:
                        pass



    def is_complement(self, base_1, base_2):
        """
        Function to determine wether bases are complentary:
        """
        Complement = False

        if base_1 == "A":
            if base_2 == "T":
                Complement = True

        if base_1 == "T":
            if base_2 == "A":
                Complement = True

        if base_1 == "G":
            if base_2 == "C":
                Complement = True

        if base_1 == "C":
            if base_2 == "G":
                Complement = True

        return Complement


#Main function that controls the script:
def main():
    infile = argv[1]
    outfile =  argv[2]
    length = int(argv[3])

    Input_Fasta = Fasta_File(infile)
    Input_Dict = Kmer_Dict(Input_Fasta.get_kmers(length))
    Input_Dict.find_primer_regions()
    primer_dict = Input_Dict.get_primers()
    good_primer_dict = Input_Dict.check_primers(primer_dict)

#Main Switch:
if __name__ == "__main__":
    main()
