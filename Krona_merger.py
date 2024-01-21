"""
This script is used to merge multiple krona files into a taxonomy table.
"""

from sys import argv

def merge_krona_files(input_dir, output_dir):
    """
    This function merges several Krona plot taxonomy files:
    """
    #Import statements:
    from os import listdir

    file_list = list(listdir(input_dir))
    merge_done = "merged_krona_file.tsv" in file_list

    if merge_done == True:
        return
    else:
        with open(output_dir + "merged_krona_file.tsv", "w") as outfile:
            for file in file_list:
                with open(input_dir + file, "r") as reader:
                    for line in reader:
                        outfile.write(file + '|' + line)

def make_krona_table(output_dir, depth):
    """
    This function makes a table out of the merged krona files.
    """
    entries = []
    levels = ["Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species"]

    with open(output_dir + "merged_krona_file.tsv") as merged_file:
        entries.append(levels[0:depth])
        for line in merged_file:
            entrie = line.split("\t")[0].split("|")[1::]
            if len(entrie) == (depth):
                if entries.count(entrie) == 0:
                    entries.append(entrie)
                else:
                    continue
            sample = line.split("|")[0]
            if entries[0].count(sample) == 0:
                entries[0].append(sample)

    return entries

def get_scores(output_dir, krona_table):
    """
    This function fills out the scores of the Krona table.
    """

    with open(output_dir + "merged_krona_file.tsv") as merged_file:
        for line in merged_file:
            print(line)


def main():
    input_dir = argv[1]
    output_dir = argv[2]
    depth = 2
    merge_krona_files(input_dir, output_dir)
    krona_table = make_krona_table(output_dir, depth)
    krona_table_scored = get_scores(output_dir, krona_table)

if __name__ == "__main__":
    main()
