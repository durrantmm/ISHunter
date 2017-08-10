configfile: "config.yml"
import os
from os.path import basename, join, dirname

WD = config['wd']
CONTIG_DIR = join(WD, config['contig_dir'])
FILT_CONTIG_DIR = join(WD, config['filtered_contig_dir'])
IR_DIR = join(WD, config['inverted_repeats'])
IR_FILTERED_CONTIG_DIR = join(WD, config['ir_filtered_contigs'])
BLAST_DIR = join(WD, config['blast_dir'])
GENBANK_DIR = join(WD, config['genbank_dir'])
TRANSPOSASE_DIR = join(WD, config['transposase_dir'])



WC = glob_wildcards(os.path.join(CONTIG_DIR, "{sample}.fasta"))

SAMPLES = WC.sample


rule all:
    input:
        expand('{transposase_dir}/{{sample}}.txt'.format(transposase_dir=TRANSPOSASE_DIR), sample=SAMPLES)
    run:
	    print("ISHUNTER FINISHED WITH NO EXCEPTIONS!")


rule filter_contigs:
    input:
        '{contig_dir}/{{sample}}.fasta'.format(contig_dir=CONTIG_DIR)
    output:
        '{filt_contig_dir}/{{sample}}.fasta'.format(filt_contig_dir=FILT_CONTIG_DIR)
    params:
        min_length=200,
        max_length=4000,
        num_sdevs_above=5
    shell:
        "python scripts/filter_contigs.py {input} {params.min_length} {params.max_length} {params.num_sdevs_above} > {output}"


rule find_inverted_repeats:
    input:
        '{filt_contig_dir}/{{sample}}.fasta'.format(filt_contig_dir=FILT_CONTIG_DIR)
    output:
        outfile='{ir_dir}/{{sample}}.inv'.format(ir_dir=IR_DIR),
        outseq='{ir_dir}/{{sample}}.fasta'.format(ir_dir=IR_DIR)
    params:
        # See ISQuest and ISScan
        gap=-5,
        threshold=10,
        match=1,
        mismatch=-2
    shell:
        'einverted {input} -gap {params.gap} -threshold {params.threshold} -match {params.match} -mismatch {params.mismatch} -outfile {output.outfile} -outseq {output.outseq}'


rule filter_contigs_inverted_repeats:
    input:
        inv_fasta='{ir_dir}/{{sample}}.fasta'.format(ir_dir=IR_DIR),
        filt_contig='{filt_contig_dir}/{{sample}}.fasta'.format(filt_contig_dir=FILT_CONTIG_DIR)
    output:
        '{outdir}/{{sample}}.fasta'.format(outdir=IR_FILTERED_CONTIG_DIR)
    shell:
        'python scripts/filter_inverted.py {input.inv_fasta} {input.filt_contig} > {output}'


rule blastx_contigs:
    input:
        '{outdir}/{{sample}}.fasta'.format(outdir=IR_FILTERED_CONTIG_DIR)
    output:
        outblast='{blast_dir}/{{sample}}.txt'.format(blast_dir=BLAST_DIR)
    params:
        db=config['blastdb']
    threads:
        config['blast_threads']
    shell:
        "blastx -db {params.db} -query {input} -out {output.outblast} -outfmt \“10 qseqid sseqid qstart qend sstart send\” -num_threads {threads}"


rule download_genbank:
    input:
        blast_results=expand('{blast_dir}/{{sample}}.txt'.format(blast_dir=BLAST_DIR), sample=SAMPLES)
    output:
        outdir=GENBANK_DIR,
        report='{genbank_dir}/complete.txt'.format(genbank_dir=GENBANK_DIR)
    shell:
        "python scripts/download_genbank.py %s {output.outdir} ; touch {output.report}" % BLAST_DIR


rule identify_transposases:
    input:
        blast_results='{blast_dir}/{{sample}}.txt'.format(blast_dir=BLAST_DIR),
        report='{genbank_dir}/complete.txt'.format(genbank_dir=GENBANK_DIR),
        genbank_dir=GENBANK_DIR

    output:
        '{transposase_dir}/{{sample}}.txt'.format(transposase_dir=TRANSPOSASE_DIR)
    shell:
        'python scripts/is_transposase.py {input.blast_results} {input.genbank_dir} > {output}'
