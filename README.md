# eVIDENCE

A software to indetify rare variants from molecular-barcoded targeted sequencing data

Overview
1. Process a bam file using Conner, and detect candidate variants
2. Remove barcode and stem sequences from a raw bam file, and generate a new bam file 
3. Filter candidate variants using a newly-created bam file

## Requirement
bwa (0.7.15 or higher)

samtools (0.1.18 or higher)

Connor (https://github.com/umich-brcf-bioinf/Connor)

perl (5 or higher)

python (3 or higher)

## Input file format
**FASTQ files**

**bed file**; file defining the captured regions

\<chr\> \<start\> \<end\>

chr1    16174529        16174663

## Output file format
**eVIDENCE.snv.vcf/ eVIDENCE.indel.vcf**

\<chr\> \<start\> \<end\> \<reference\> \<variant\> \<total number of reads\> \<number of variant reads\> \<variant allele frequency (%)\>

1       16256435        16256435        G       A       1221    3       0.2457002457002457

16      72821636        72821638        ACT     -       869     8       0.9205983889528193

## Usage
**config file**; Please enter path to reference.fasta file (prefix "chr" is required), bwa, samtools, Connor and bed file. 
If you want to change parameters, please change this file (see below)).

```
sh eVIDENCE.sh FASTQ1 <Path to fastq1> FASTQ2 <Path to fastq2> OUT <Output directory name> SAMPLE_NAME <Sample name>
```

## Parameter setting in configuration file
If you would like to use different parameters, please make changes in the config file. 


VAF_SNV; Minimum variant allele frequency for SNV calling (0.001)

NUM_SNV; Minimum number of reads for SNV calling (3)

Q_score; Minimum quality score of a base call (20)

VAF_INDEL; Minimum variant allele frequency for indel calling (0.001)

NUM_INDEL; Minimum number of reads for indel calling (3)

MIN_DEPTH; Minimum depth (100)


\##Connor params## (see https://github.com/umich-brcf-bioinf/Connor)

CONSENSUS_FREQ_THRESHOLD (0.6)

MIN_FAMILY_SIZE_THRESHOLD (3)

UMT_DISTANCE_THRESHOLD (1)

## Performance


## Licence
GPL

## Contact

Kei Mizuno - km1207@kuhp.kyoto-u.ac.jp

## Update
