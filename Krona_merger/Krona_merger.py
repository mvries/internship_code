"""
This script is used to merge multiple krona files into a taxonomy table.

To Run:
python3 Krona_merger.py input_path/ output_path/ desired_depth

Note: Depth refers to the taxonomic level depth:
1 = Kingdom
2 = Phyla
3 = Class
4 = Order
5 = Family
6 = Genus
7 = Species

Author: Martijn de Vries (m97devries@gmail.com)
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

    for entrie in entries[1::]:
        for i in range(depth, len(entries[0])):
            entrie.append(0)

    return entries

def get_scores(output_dir, krona_table, depth):
    """
    This function fills out the scores of the Krona table.
    """
    with open(output_dir + "merged_krona_file.tsv") as merged_file:
        for line in merged_file:
            sample = line.split("|")[0]
            sample_position = krona_table[0].index(sample)
            entrie = line.split("\t")[0].split("|")[1::]
            score = line.split("\t")[-1].strip("\n")

            if len(entrie) == depth:
                position = 0
                for entrie_2 in krona_table:
                    entrie_stripped = entrie_2[0:depth]

                    if entrie_stripped == entrie:
                        krona_table[position][sample_position] = score
                    else:
                        position += 1

    return krona_table

def print_table(output_dir, krona_table):
    """
    This function prints the krona table in TSV format.
    """

    for entrie in krona_table:
        outstring = ""
        for sub_entrie in entrie:
            outstring += str(sub_entrie) + "\t"
        outstring.strip("\t")

        with open(output_dir + "krona_table.tsv", "a") as outfile:
            outfile.write(outstring + "\n")

def main():
    input_dir = argv[1]
    output_dir = argv[2]
    depth = int(argv[3])
    merge_krona_files(input_dir, output_dir)
    krona_table = make_krona_table(output_dir, depth)
    krona_table_scored = get_scores(output_dir, krona_table, depth)
    print_table(output_dir, krona_table_scored)

if __name__ == "__main__":
    main()
