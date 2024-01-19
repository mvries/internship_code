"""
This script is used to merge multiple krona files into a taxonomy table.
"""

from sys import argv
from os import listdir


def make_table(input_dir, outfile):
    """
    This function is used to make a taxonomy table from multiple krona files.
    """
    file_list = list(listdir(input_dir))

    #First the files are merged into one file
    with open(input_dir + "merged_krona_file.tsv", "w") as outfile:
        for file in file_list:
            with open(input_dir + file, "r") as reader:
                for line in reader:
                    outfile.write(line)

    #Then a table is made from the merged file:
    table_dict = {}

    with open(input_dir + "merged_krona_file.tsv", "r") as merged_file:
        for line in merged_file:

            identifier = line.split("\t")[0]
            entries = identifier.split("|")



            for entrie in entries:
                if entrie not in table_dict.keys():
                    table_dict[entrie] = {}

            print(table_dict)







def main():
    input_dir = argv[1]
    make_table(input_dir, "test")

if __name__ == "__main__":
    main()
