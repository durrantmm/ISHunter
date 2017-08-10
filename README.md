# ISHunter

## Contents
* [Introduction](#introduction)
* [Installation](#installation)
	* [Download ISHunter](#download-ishunter)
	* [Install ISHunter](#install-ishunter)
	* [Test Installation](#test-installation)
* [Preparing Input Files](#preparing-input-files)

## Introduction
The ISHunter workflow is designed to...
1. Filter the contigs with a specified range of lengths and coverage cutoff, and then extract the contigs with inverted repeats.
2. Run blastx on the contigs.
3. From the blastx results, download the corresponding genbank files.
4. Identify mobile elements.

## Installation
ISHunter is implemented as a snakemake workflow. Snakemake is a workflow management system that allows for all the tasks to be easily parallelized. We strongly recommend that you read about snakemake and even complete the beginner's tutorial [here](https://snakemake.readthedocs.io/en/stable/).

This pipeline requires you to create a conda environment so that you can then easily download all of the required packages and run the workflow on any system you'd like. If you haven't already, download anaconda [here](https://www.continuum.io/downloads). We strongly suggest that you learn the basics of anaconda before continuing with installation.

### Download ISHunter
From a unix terminal, type the following:

~~~~
git clone https://github.com/durrantmm/ISHunter.git
cd ISHunter
~~~~

You are now in the downloaded `ISHunter` directory.

### Install ISHunter
Let's now create a conda environment from the provided `environment.yaml` in the `ISHunter` directory:

~~~~
conda env create -f environment.yaml
~~~~

You can then activate the `ISHunter` conda environment with the command:

~~~~
source activate ISHunter
~~~~

### Test Installation
`ISHunter` should now be ready to go, but first let's test the installation.
From the `ISHunter` directory, run

~~~~
snakemake --config output_dir=test -p
~~~~

After a few seconds of running, you should see the process end with the message

~~~~
ISHUNTER FINISHED WITH NO EXCEPTIONS!
~~~~

`ISHunter` should now be properly installed.

## Preparing Input Files
Create a directory called `0.contigs`:

~~~~
mkdir 0.contigs
cd 0.contigs
~~~~

You are now in the `0.contigs` directory. Move your completed metagenomic assembly files (<...>.fasta) files here. 

### Bugs
Please submit problems or requests here: https://github.com/durrantmm/ISHunter/issues
