"""
This is a python wrapper that controls the rarefraction maker.
"""

import subprocess
from sys import argv


def quality_check():
    """
    This function performs a quality check of the input reads:
    """

    cmd = "fastp -f 20 -F 20 -i " + fastq1 + " -I " + fastq2 + " -o " + output_dir + "/tmp/" \
    + "trimmed_1.fq" + " -O " + output_dir + "/tmp/" + "trimmed_2.fq"

    subprocess.check_call(cmd, shell=True)

    trimmed_1 = output_dir + "/tmp/" + "trimmed_1.fq"
    trimmed_2 = output_dir + "/tmp/" + "trimmed_2.fq"

    return trimmed_1, trimmed_2

def sample_reads(trimmed_1, trimmed_2):
    """
    This function makes samples of reads
    """

    fractions = [i for i in range(10000,100000, 10000)]

    for fraction in fractions:

        try:
            cmd = "mkdir " + output_dir + "/tmp/" + "fraction_" + str(fraction)
            subprocess.check_call(cmd, shell=True)
        except:
            pass

        cmd = "seqtk sample -s100 " + trimmed_1 + " " + str(fraction) + " > " +\
        output_dir + "tmp/fraction_" + str(fraction) + "/file1.fq"
        subprocess.check_call(cmd, shell=True)

        cmd = "seqtk sample -s100 " + trimmed_2 + " " + str(fraction) + " > " +\
        output_dir + "tmp/fraction_" + str(fraction) + "/file2.fq"
        subprocess.check_call(cmd, shell=True)

def merge_reads():
    """
    This function assembles/merges the paired end reads
    """

    fractions = [i for i in range(10000,100000, 10000)]

    for fraction in fractions:
        cmd = "flash -M 250 -m 50 -d " + output_dir + "/tmp/fraction_" + str(fraction) + "/ "\
        + output_dir + "tmp/fraction_" + str(fraction) + "/file1.fq "\
        + output_dir + "tmp/fraction_" + str(fraction) + "/file2.fq "
        subprocess.check_call(cmd, shell=True)


#Main function:
def main():
    print("Making rarefraction curve!")

    try:
        cmd = "mkdir " + output_dir + "tmp"
        subprocess.check_call(cmd, shell=True)
    except:
        pass

    trimmed_1, trimmed_2 = quality_check()
    sample_reads(trimmed_1, trimmed_2)
    merge_reads()


#Main switch
if __name__ == "__main__":
    fastq1 = argv[1]
    fastq2 = argv[2]
    output_dir = argv[3]
    main()


    """
    flash -o output_dir mate1.fq mate2.fq
    """
