#!/bin/bash
esearch -db nucleotide -query "$1" | efetch -format fasta
