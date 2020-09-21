# primer-schemes

Primer schemes for real-time genome epidemiology

[![Build Status](https://travis-ci.org/artic-network/primer-schemes.svg?branch=master)](https://travis-ci.org/artic-network/primer-schemes)
[![DOI](https://zenodo.org/badge/96756353.svg)](https://zenodo.org/badge/latestdoi/96756353)

## About

The primer schemes in this repository were built using [Primal Scheme](https://primalscheme.com/) and are available for the following viruses:

- Ebola
- Nipah
- SARS-CoV-2 (nCoV-2019)

Within each virus directory, there are versioned sub-directories which each contain a versioned scheme for that virus.

The following files are available per scheme version:

| file extension     | about                                                                                  |
| ------------------ | -------------------------------------------------------------------------------------- |
| `.primer.bed`      | The coordinates of each primer in the scheme                                           |
| `.insert.bed`      | The coordinates of the expected amplicons that the scheme produces (excluding primers) |
| `.reference.fasta` | The sequence of the reference genome used for the scheme                               |
| `.tsv`             | Details on each primer in the scheme (name, sequence, length, GC, TM)                  |

For more information visit the [ARTIC network website](https://artic.network/).

## Notes

- There may be some additional files in the scheme directories - these are either deprecated and left for backward compatibility (e.g. `scheme.bed`), or are created by Primal Scheme [check here](https://github.com/aresti/primalscheme) for more info.
- The schemes are in BED format, which is a 0-based, half-open format. This means that reference sequence position counting starts at 0 and the chromEnd is not included in the primer sequence.
- All the schemes within this repository can be downloaded using [artic-tools](https://github.com/will-rowe/artic-tools) (e.g. `artic-tools get_scheme ebola --schemeVersion 2`)
- The SARS-CoV-2 directory is an alias to the original nCoV-2019 directory, left for backwards compatibility

## Updated scheme file format

> updated: 25.08.2020

### changes

With the major version bump to [Primal Scheme](https://github.com/aresti/primalscheme), primer schemes are now output to `*.primer.bed` files.

These new files aren't much different to the old `*.scheme.bed` files and the same information is contained within, but they now conform to the [BED standard](https://genome.ucsc.edu/FAQ/FAQformat.html#format1).

The new format has the following columns:

| column | name       | type         | description                                               |
| ------ | ---------- | ------------ | --------------------------------------------------------- |
| 1      | chrom      | string       | primer reference sequence                                 |
| 2      | chromStart | int          | starting position of the primer in the reference sequence |
| 3      | chomEnd    | int          | ending position of the primer in the reference sequence   |
| 4      | name       | string       | primer name                                               |
| 5      | primerPool | int          | primer pool<sup>\*</sup>                                  |
| 6      | strand     | string (+/-) | primer direction                                          |

<sup>\*</sup> column 5 in the BED spec is an int for score, whereas here we are using it to denote primerPool.

### commands

The `liftover.py` script was used to create a `*.primer.bed` file for each `*.scheme.bed` file, within each scheme directory in this repository.

The `validate_scheme` command from [artic-tools](https://github.com/will-rowe/artic-tools) was used to validate each `*.primer.bed` and also to create the `*.insert.bed` file which is produced by recent versions of [Primal Scheme](https://github.com/aresti/primalscheme).

The following commands where used:

```bash
for i in */V*/*.scheme.bed;
do
basename=${i%%.scheme.bed}
scripts/liftover.py -i $i -o ${basename}.primer.bed;
artic-tools validate_scheme ${basename}.primer.bed --outputInserts ${basename}.insert.bed
done;
```
