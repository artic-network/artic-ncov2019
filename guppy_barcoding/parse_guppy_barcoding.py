import argparse
from Bio import SeqIO

def parse_args():
    parser = argparse.ArgumentParser(description='Parse barcode info and minimap paf file, create report.')

    parser.add_argument("--paf_file", action="store", type=str, dest="paf_file")
    parser.add_argument("--reads", action="store", type=str, dest="reads")

    parser.add_argument("-o", action="store", type=str, dest="outdir")

    parser.add_argument("-b", action="store", type=str, dest="barcode")

    parser.add_argument("-n", action="store", type=float, dest="min_length")
    parser.add_argument("-x", action="store", type=float, dest="max_length")

    return parser.parse_args()

def parse_line(line):
    values = {}
    tokens = line.rstrip('\n').split('\t')

    return (tokens[0], tokens[5])

def parse_paf(paf):

    mapped_reads = []

    with open(str(paf),"r") as f:
        for line in f:

            read_name, ref_hit = parse_line(line)

            if ref_hit != '*':
                mapped_reads.append(read_name)

    return mapped_reads
    

def write_only_mapped_reads(reads, output_reads, mapped_list, min_length, max_length)
    written = 0 
    records_to_write = []
    for record in SeqIO.parse(reads, "fastq"):
        if record.id in mapped_list:
            if len(record)>=min_length and len(record)<=max_length:
                records_to_write.append(record)
                written +=1
    with open(output_reads,"w") as handle:
        SeqIO.write(records_to_write, handle, "fastq")

    return len(records_to_write), written

def filter_reads(reads, output_reads, paf, min_length, max_length):

    counts, mapped_list = parse_paf(paf)

    total, num_reads_written = write_only_mapped_reads(reads, output_reads, mapped_list, min_length, max_length)

    print(f"Found a total of {total} reads in {reads}.\n")
    print(f"{num_reads_written} written to {output_reads}.")

if __name__ == '__main__':

    args = parse_args()

    output_reads= None
    if str(args.outdir)=="" or not args.outdir:
        output_reads = "binned_{args.barcode}.fastq"
    else:
        output_reads = args.outdir + "/binned_{args.barcode}.fastq"

    filter_reads(args.reads, output_reads, args.paf, float(args.min_length), float(args.max_length))
