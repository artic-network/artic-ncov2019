---
title: "nCoV-2019 novel coronavirus Nanopore sequencing bioinformatics protocol | amplicon, native barcoding"
keywords: protocol
layout: document
last_updated: Jan 23, 2020
tags: [protocol]
permalink: /ncov-2019/ncov2019-bioinformatics-sop.html
folder: ncov
title_text: "nCoV-2019 novel coronavirus bioinformatics protocol"
subtitle_text: "Nanopore | bioinformatics"
document_name: "ARTIC-nCoV-bioinformaticsSOP"
version: v1.0.0
creation_date: 2020-01-23
forked_from: 
author: Nick Loman, Andrew Rambaut, Aine O'Toole
citation: "Loman *et al.* In Prep."
nav_menu: false
show_tile: false
category: ncov
---

{% include callout.html
type='default'
content='**Overview:** A complete bioinformatics protocol to take the output from the [sequencing protocol](/ebov/ebov-seq-sop.html) to consensus genome sequences. Includes basecalling, de-multiplexing, mapping, polishing and consensus generation.
'
%}

## Preparation

Set up the computing environment as described here in this document: [ncov2019-it-setup](ncov2019-it-setup.html). This should be done and tested prior to sequencing, particularly if this will be done in an environment without internet access or where this is slow or unreliable. Once this is done, the bioinformatics can be performed largely off-line. If you are already using the [lab-on-an-SSD](https://github.com/artic-network/fieldbioinformatics/tree/master/lab-on-an-ssd), you can skip this step.


### Activate the ARTIC environment:

All steps in this document should be performed in the ```artic-pipeline``` conda environment:

```bash
source activate artic-pipeline
```

### Make a new directory for analysis

Give your run directory a meaningful name, e.g.. minion_run1

```bash
mkdir run_name
cd run_name

```
## Step 1: Basecalling

### Basecalling with MinKNOW (live)
When running the MinION, basecalling can be run live using MinKNOW. Particularly if you're planning on running RAMPART, this is the most sensible option. guppy GPU basecalling will keep up with the rate of data production and let you see read coverage of your sample increasing in real-time. The best ways to run guppy GPU basecalling are with a MinIT or using the ARTIC-Network [lab-on-an-SSD](https://github.com/artic-network/lab-on-an-SSD) on a gpu-laptop.  

### Basecalling with Guppy 

If you did live basecalling with MinKNOW, you can skip this step.

Otherwise, run the Guppy basecaller on the new MinION run folder:

For fast mode basecalling:

```bash
guppy_basecaller -c dna_r9.4.1_450bps_fast.cfg -i /path/to/reads -s run_name -x auto -r
```

For high-accuracy mode basecalling:

```bash
guppy_basecaller -c dna_r9.4.1_450bps_hac.cfg -i /path/to/reads -s run_name -x auto -r
```

You need to substitute `/path/to/reads` to the folder where the FAST5 files from your
run are. Common locations are:

   - Mac: ```/Library/MinKNOW/data/run_name```
   - Linux: ```/var/lib/MinKNOW/data/run_name```
   - Windows ```c:/data/reads```
   
This will create a folder called `run_name` with the base-called reads in it.

## Step 2: Data analysis

Double check you're in the correct directory (Hint: type ``pwd`` into your terminal). You should be in your MinION run directory.

Make a directory for you to put your analysis and navigate into it.

```
mkdir analysis
cd analysis
```

### *Optional* setup for RAMPART
Recommended: you can just do this step in the file browser! 

Use the template in ``examples`` to generate the ``barcodes.csv``. Double click on the file in ``examples`` to open it, click the button with three lines and click “Save as”. Save this file inside your ``run_name/analysis`` directory that you’ve just made, keep the same name.

Replace the barcodes and sample names in the ``barcodes.csv`` template with the ones from your MinION run. Make sure your sample names don’t have spaces in them and are unique! 

Use the template in ``examples`` to generate the ``run_configuration.json``. 

Replace the example path with the path to your basecalled reads (i.e. fastq files). 

#### Do you know where your basecalled reads are?

Explore where MinKNOW has put the data from your run (use the terminal).

Hint: press the Tab key to autocomplete the directory names. 

Type:

```
ls /var/lib/MinKNOW/data (*Hint*: press tab, tab, tab, tab ...)
```

Fill in the path with tab until you see fastq_pass as one of the directories.

```
cd /var/lib/MinKNOW/data/run_name/.../.../fastq_pass
```

where /.../.../ represents the string of letters and numbers MinKNOW generates for each run. The run_name will be whatever you told MinKNOW your run name was.

It is important to be able to find this data in order to do the bioinformatic analysis. In this directory, you will find four directories containing the FAST5 files and also the FASTQ files, with a pass and fail directory for each of them.

### Running RAMPART

Navigate to the directory run_name/analysis.

Ensure you have activated the conda environment (``conda activate artic-pipeline``) and then simply type:

```
rampart --protocol ~/artic-ncov2019/rampart --basecalledPath /path/to/reads/
```

In a web browser, navigate to localhost:3000 to view your samples on RAMPART.
(Note: this does not require an internet connection)  

If you completed the optional setup and you have a run_configuration.json file, you can omit the --basecalledPath argument from the command line, provided you are in the analysis directory.

### Setup for consensus generation

Open a new terminal window and navigate to your run directory again e.g. minion_run1.

```
cd minion_run1/analysis
```

If RAMPART has run successfully you will see a directory has been created in here called ``annotations`` (Hint: type ``ls`` to see if this directory exists).

### Quick usage: Generate a consensus sequence using the ARTIC pipeline

Provided you have a run_configuration.json file:

If you haven't used barcodes and are just running one sample, simply type:

```
postbox -p ~/artic-ncov2019
```

If not, run:

```
postbox -p ~/artic-ncov2019 --basecalled_path 
```

Substitute in the appropriate ``path/to/fastq_pass`` for your particular run. If you have not run basecalling with MinKNOW, you will have to also specify where your fast5 files are. 

```
postbox -p ~/artic-ncov2019 basecalled_path=path/to/fastq_pass fast5_path=path/to/fast5_pass
```

### Quick usage: Generate a consensus sequence for each barcode using the ARTIC pipeline
e.g. to run the ARTIC pipeline for barcodes NB01, NB02 and NB03

```
postbox -p ~/artic-ncov2019 basecalled_path=path/to/fastq_pass barcodes=NB01,NB02,NB03
```

or: 

```
snakemake --snakefile ~/artic-ncov2019/rampart/pipelines/get_consensus/Snakefile \
--config \
basecalled_path=path/to/fastq_pass \
annotated_path=./annotations \
barcodes=NB01,NB02,NB03
```

### Detailed usage: 1) Binning


Double check you're in the ``analysis`` directory (type ``pwd``). 

To make use of the output of RAMPART, run BinLorry to extract the binned read files:

```
binlorry -i path/to/fastq_pass \
-t ../annotations \
-o ./binned \
-n 400 \
-x 700 \
--bin-by barcode \
--filter-by barcode NB01 NB02 NB03 \
--filter-by best_reference nCoV2019 \
--force-output \
--out-report
```

BinLorry will iterate through your files and create a binned fastq and csv file for each barcode specified. e.g. for barcodes NB01, NB02 and NB03, the files produced will be:
binned_NB01.fastq
binned_NB02.fastq
binned_NB03.fastq
and a corresponding csv file.

### Detailed usage: 2) Gather

We then collect all the FASTQ files (typically stored in files each containing 4000 reads) into a single file.

```
artic gather --min-length 400 --max-length 700 --prefix run_name
```
The command will show you the runs in /var/lib/MinKNOW/data and ask you to select one. If you know the path to the reads use:

```
artic gather --min-length 400 --max-length 700 --prefix run_name --directory /path/to/reads
```

Here /path_to_reads should be the folder in which MinKNOW put the base-called reads (i.e., run_name from the command above).

We use a length filter here of between 400 and 700 to remove obviously chimeric reads.

You will now have a file called: run_name_fastq_pass.fastq and a file called run_name_sequencing_summary.txt, as well as individual files for each barcode (if previously demultiplexed).

### Detailed usage: 3) Create the nanopolish index:

```bash
nanopolish index -s run_name_sequencing_summary.txt -d /path/to/fast5_pass run_name_fastq_pass.fastq
```

Again, alter ``/path/to/fast5_pass`` to point to the location of the FAST5 files.

### Detailed usage: 4) Run the MinION pipeline

For each barcode you wish to process (e.g. run this command 12 times for 12 barcodes), replacing the file name and sample name as appropriate:

E.g. for NB01

```bash
artic minion --normalise 200 --threads 4 --scheme-directory ~/artic-ncov2019/primer-schemes --read-file binned_NB01.fastq --nanopolish-read-file run_name_pass.fastq nCoV-2019/V1 sample1
```

Replace ``sample1`` as appropriate.

E.g. for NB02

```bash
artic minion --normalise 200 --threads 4 --scheme-directory ~/artic/artic-ncov2019/primer-schemes --read-file binned_NB02.fastq --nanopolish-read-file run_name_pass.fastq nCoV-2019/V1 sample2
```

## ARTIC MinION Output files

   * ``sample1.primertrimmed.bam`` - BAM file for visualisation after primer-binding site trimming
   * ``sample1.vcf`` - detected variants in VCF format
   * ``sample1.variants.tab`` - detected variants
   * ``sample1.consensus.fasta`` - consensus sequence

To put all the consensus sequences in one filei called my_consensus_genome, run

```bash
cat *.consensus.fasta > my_consensus_genomes.fasta
```

## Step 3: Visualise genomes in Tablet

Open a new Terminal window:

```bash
conda activate tablet
tablet
```

Go to "Open Assembly"

Load the BAM (binary alignment file) as the first file.

Load the refernece file (in artic/artic-ncov2019/primer_schemes/nCoV-2019/V1/nCoV-2019.reference.fasta) as the second file.

Select Variants mode in Color Schemes for ease of viewing variants.

## Experimental Medaka pipeline

An alternative to nanopolish to calling variants is to use medaka. Medaka is faster than nanopolish and seems to perform mostly equivalently in (currently limited) testing.

You'll need a different environment for Medaka, as it can't happily co-exist with nanopolish:

```
conda env create -f artic-ncov2019-medaka.yaml
```

```
source activate artic-ncov2019-medaka
``

If you want to use Medaka, you can skip the ``nanopolish index`` step, and add the parameter ``--medaka`` to the command, as below:

```bash
artic minion --medaka --normalise 200 --threads 4 --scheme-directory ~/artic-ncov2019/primer-schemes --read-file run_name_pass_NB01.fastq nCoV-2019/V1 samplename
```

Replace ``samplename`` as appropriate.

E.g. for NB02

```bash
artic minion --medaka --normalise 200 --threads 4 --scheme-directory ~/artic/artic-ncov2019/primer-schemes --read-file run_name_pass_NB02.fastq nCoV-2019/V1 samplename
```

## Using minimap2 instead of bwa

It is possible to use ``minimap2`` in the pipeline instead of ``bwa`` by adding ``--minimap2`` as a parameter to ``artic minion``.

