"""
This is a python wrapper that controls the rarefraction maker.
"""

import subprocess
from sys import argv


def quality_check():
    """
    This function performs a quality check of the input reads:
    """

    cmd = "fastp -i " + fastq1 + " -I " + fastq2 + " -o " + output_dir + "tmp/" \
    + "trimmed_1.fq" + " -O " + output_dir + "tmp/" + "trimmed_2.fq"

    subprocess.check_call(cmd, shell=True)

    trimmed_1 = output_dir + "tmp/" + "trimmed_1.fq"
    trimmed_2 = output_dir + "tmp/" + "trimmed_2.fq"

    return trimmed_1, trimmed_2

def sample_reads(trimmed_1, trimmed_2):
    """
    This function makes fractional samples of reads
    """

    fractions = [i for i in range(1,10)]

    for fraction in fractions:

        try:
            cmd = "mkdir " + output_dir + "tmp/" + "fraction_" + str(fraction)
            subprocess.check_call(cmd, shell=True)
        except:
            pass

        cmd = "seqtk sample -s100 " + trimmed_1 + " 0." + str(fraction) + " > " +\
        output_dir + "tmp/fraction_" + str(fraction) + "/file1.fq"
        subprocess.check_call(cmd, shell=True)

        cmd = "seqtk sample -s100 " + trimmed_2 + " 0." + str(fraction) + " > " +\
        output_dir + "tmp/fraction_" + str(fraction) + "/file2.fq"
        subprocess.check_call(cmd, shell=True)

def merge_reads():
    """
    This function assembles/merges the paired end reads
    """

    fractions = [i for i in range(1,10)]

    for fraction in fractions:
        cmd = "flash -M 250 -d " + output_dir + "tmp/fraction_" + str(fraction) + "/ "\
        + output_dir + "tmp/fraction_" + str(fraction) + "/file1.fq "\
        + output_dir + "tmp/fraction_" + str(fraction) + "/file2.fq "

        print(cmd)

        subprocess.check_call(cmd, shell=True)


#Main function:
def main():
    print("Making rarefraction curve!")

    try:
        cmd = "mkdir " + output_dir + "tmp/"
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
