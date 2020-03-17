# artic-ncov2019

Initial implementation of an ARTIC bioinformatics platform for nanopore sequencing of nCoV2019 novel coronavirus.
This pipeline is setup to run in conjunction with RAMPART. It accesses the barcoding and mapping information from the RAMPART output and uses this to bin reads. It then spawns off Nick Loman's ARTIC MinION pipeline to run nanopolish. It's final output is to take the consensus sequences for each barcode, give the sequence headers the sample name with other metadata about the sequence (length, barcode, number of N's) and compiles them into a single fasta file found in the ``consensus_sequences`` directory produced. There is also some compatibility with guppy barcoding, but only once the run has finished (i.e. not in real-time with RAMPART).

## Documentation
  * [Preparation](#preparation)
    * [Activate the ARTIC environment](#activate-the-artic-environment)
    * [Install postbox](#install-postbox-dependency)
    * [Make a new directory for analysis](#make-a-new-directory-for-analysis)
  * [Step 1: Basecalling](#step-1-basecalling)
    * [Basecalling with MinKNOW (live)](#basecalling-with-minknow-(live))
    * [Basecalling with Guppy](#basecalling-with-guppy)
    * [Basecalling and demultiplexing with Guppy](#basecalling-and-demultiplexing-with-guppy)
  * [Step 2: Data analysis](#step-2-data-analysis)
    * [*Optional* setup for RAMPART](#optional-setup-for-rampart)
    * [Do you know where your basecalled reads are?](#do-you-know-where-your-basecalled-reads-are)
    * [Running RAMPART](#running-rampart)
    * [Setup for consensus generation](#setup-for-consensus-generation)
  * [Quick usage](#quick-usage-generate-a-consensus-sequence-using-the-artic-pipeline)
    * [Quick usage: Generate a consensus sequence using the ARTIC pipeline](#quick-usage-generate-a-consensus-sequence-using-the-artic-pipeline)
    * [Quick usage: Generate a consensus sequence for each barcode using the ARTIC pipeline](#quick-usage-generate-a-consensus-sequence-for-each-barcode-using-the-artic-pipeline)
  * [Quick usage: Output files](#quick-usage-output-files)
  * [Detailed usage](#detailed-usage-1-binning)
     * [Detailed usage: 1) Binning](#detailed-usage-1-binning)
     * [Detailed usage: 2) Gather](#detailed-usage-2-gather)
     * [Detailed usage: 3) Create the nanopolish index](#detailed-usage-3-create-the-nanopolish-index)
     * [Detailed usage: 4) Run the MinION pipeline](#detailed-usage-4-run-the-minion-pipeline)
  * [ARTIC MinION Output files](#artic-minion-output-files)

## Preparation

Set up the computing environment as described here in this document: [ncov2019-it-setup](ncov2019-it-setup.html). This should be done and tested prior to sequencing, particularly if this will be done in an environment without internet access or where this is slow or unreliable. Once this is done, the bioinformatics can be performed largely off-line. If you are already using the [lab-on-an-SSD](https://github.com/artic-network/fieldbioinformatics/tree/master/lab-on-an-ssd), you can skip this step.


### Activate the ARTIC environment

All steps in this document should be performed in the ```artic-pipeline``` conda environment:

```bash
source activate artic-ncov2019
```

### Install postbox dependency

Postbox is a wrapper written by Rachel Colquohon that will allow complicated snakemake commands to be configured with a csv and/or json file. Install this by typing:

```bash
pip install git+https://github.com/rmcolq/postbox.git@v0.6
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

### Basecalling and demultiplexing with Guppy

Although not recommended, as RAMPART can demultiplex in real-time but is not currently compatible with guppy demultiplexing, if you have run MinKNOW with barcoding turned on, you can still run this pipeline after your run has finished.

To essentially meet the pipeline where RAMPART would have left off, do the following:

For example, to run for barcodes barcode01, barcode02 and barcode03, from the directory your demultiplexed files are in, run:

```
snakemake --snakefile ~/artic-ncov2019/guppy_barcoding/Snakefile --config barcodes=barcode01,barcode02,barcode03
```

Setup as you would for running RAMPART in the Optional setup for RAMPART (i.e. create a run_configuration.json file that points to your basecalledPath and a barcodes.csv.) and you can run postbox as you would below.

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
If you have generated a ``barcodes.csv`` and a ``run_configuration.json``, the command you run is identical to the command above:

```
postbox -p ~/artic-ncov2019
```

If not, you will need to specify extra information in the command.
e.g. to run the ARTIC pipeline for barcodes NB01, NB02 and NB03

```
postbox -p ~/artic-ncov2019 basecalled_path=path/to/fastq_pass barcodes=NB01,NB02,NB03
```

### Quick usage: Output files

There is detailed information about the output files produced below, but when running through ``postbox`` a directory called ``consensus_sequences`` is produced with a single .fasta file containing all the sequences generated by the pipeline, with sample name, barcode and sequence length annotated in the read header.

```
consensus_sequences/run_name.fasta
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

### Detailed usage: 3) Create the nanopolish index

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

