#!/bin/bash

path=$0

if [ "$path" == "${path%/*}" ]; then
	SRC=.
else
	SRC=${path%/*}
fi

FASTQ1=$1
FASTQ2=$2
OUT=$3
FILE_NAME=$4

REF=`python $SRC/bin/read_config.py $SRC/config REF`
BWA=`python $SRC/bin/read_config.py $SRC/config BWA`
SAMtools=`python $SRC/bin/read_config.py $SRC/config SAMtools`
Connor=`python $SRC/bin/read_config.py $SRC/config Connor`

BED=`python $SRC/bin/read_config.py $SRC/config BED`
VAF_SNV=`python $SRC/bin/read_config.py $SRC/config VAF_SNV`
NUM_SNV=`python $SRC/bin/read_config.py $SRC/config NUM_SNV`
Q_socre=`python $SRC/bin/read_config.py $SRC/config Q_socre`
VAF_INDEL=`python $SRC/bin/read_config.py $SRC/config VAF_INDEL`
NUM_INDEL=`python $SRC/bin/read_config.py $SRC/config NUM_INDEL`
MIN_DEPTH=`python $SRC/bin/read_config.py $SRC/config MIN_DEPTH`

CONSENSUS_FREQ_THRESHOLD=`python $SRC/bin/read_config.py $SRC/config CONSENSUS_FREQ_THRESHOLD`
MIN_FAMILY_SIZE_THRESHOLD=`python $SRC/bin/read_config.py $SRC/config MIN_FAMILY_SIZE_THRESHOLD`
UMT_DISTANCE_THRESHOLD=`python $SRC/bin/read_config.py $SRC/config UMT_DISTANCE_THRESHOLD`

$BWA mem $REF $FASTQ1 $FASTQ2 > $OUT/$FILE_NAME.sam

$SAMtools view -S -b $OUT/$FILE_NAME.sam > $OUT/$FILE_NAME.bam

$SAMtools sort $OUT/$FILE_NAME.bam $OUT/$FILE_NAME.sort

$SAMtools index $OUT/$FILE_NAME.sort.bam

$Connor -f $CONSENSUS_FREQ_THRESHOLD -s $MIN_FAMILY_SIZE_THRESHOLD -d $UMT_DISTANCE_THRESHOLD $OUT/$FILE_NAME.sort.bam $OUT/$FILE_NAME.connor.bam

$SAMtools mpileup -s -f $REF $OUT/$FILE_NAME.connor.bam > $OUT/$FILE_NAME.connor.pile

perl $SRC/bin/SNP_frqQ_caller.pl -Infile $OUT/$FILE_NAME.connor.pile -INDEL /dev/null -SNV /dev/stdout -cut_off_frq $VAF_SNV -cut_off_num $NUM_SNV -cut_off_Q $Q_score -indel_allele_num_cutoff 1 -indel_allele_frq_cutoff 0.5 > $OUT/$FILE_NAME.connor.pile.snv

perl $SRC/bin/SNP_frqQ_caller.pl -Infile $OUT/$FILE_NAME.connor.pile -INDEL /dev/stdout -SNV /dev/null -cut_off_frq 0.005 -cut_off_num 5 -cut_off_Q $Q_score -indel_allele_num_cutoff $NUM_INDEL -indel_allele_frq_cutoff VAF_INDEL > $OUT/$FILE_NAME.connor.pile.indel

python $SRC/bin/target.py $BED $OUT/$FILE_NAME.connor.pile.snv > $OUT/$FILE_NAME.connor.pile.target.snv

python $SRC/bin/target.py $BED $OUT/$FILE_NAME.connor.pile.indel > $OUT/$FILE_NAME.connor.pile.target.indel

python $SRC/bin/change_snv.py $OUT/$FILE_NAME.connor.pile.target.snv > $OUT/$FILE_NAME.connor.pile.target.rev.snv

python $SRC/bin/change_indel.py $OUT/$FILE_NAME.connor.pile.target.indel > $OUT/$FILE_NAME.connor.pile.target.rev.indel

rm $OUT/$FILE_NAME.connor.pile.snv
rm $OUT/$FILE_NAME.connor.pile.target.snv
rm $OUT/$FILE_NAME.connor.pile.indel
rm $OUT/$FILE_NAME.connor.pile.target.indel

python $SRC/bin/make_new_sam_1.py $OUT/$FILE_NAME.sam > $OUT/$FILE_NAME.rev_for_fastq.ver2_1.txt

rm $OUT/$FILE_NAME.sam

python $SRC/bin/make_new_sam_2.py $OUT/$FILE_NAME.rev_for_fastq.ver2_1.txt > $OUT/$FILE_NAME.rev_for_fastq.ver2_final.txt

rm $OUT/$FILE_NAME.rev_for_fastq.ver2_1.txt

python $SRC/bin/make_fastq_1_file.py $OUT/$FILE_NAME.rev_for_fastq.ver2_final.txt > $OUT/$FILE_NAME.new_1.fastq

python $SRC/bin/make_fastq_2_file.py $OUT/$FILE_NAME.rev_for_fastq.ver2_final.txt > $OUT/$FILE_NAME.new_2.fastq

rm $OUT/$FILE_NAME.rev_for_fastq.ver2_final.txt

$BWA mem $REF $OUT/$FILE_NAME.new_1.fastq $OUT/$FILE_NAME.new_2.fastq > $OUT/$FILE_NAME.new.sam

rm $OUT/$FILE_NAME.new_1.fastq

rm $OUT/$FILE_NAME.new_2.fastq

$SAMtools view -S -b $OUT/$FILE_NAME.new.sam > $OUT/$FILE_NAME.new.bam

python $SRC/bin/add_barcode.py $OUT/$FILE_NAME.new.sam|sort -k3,3 -k4n,4 -k31,31 /dev/stdin > $OUT/$FILE_NAME.new.barcode.sort.txt

rm $OUT/$FILE_NAME.new.sam

python $SRC/bin/separate_chr.py $OUT/$FILE_NAME.new.barcode.sort.txt $OUT/$FILE_NAME.new.barcode.sort.

rm $OUT/$FILE_NAME.new.barcode.sort.txt

for variant in `cat $OUT/$FILE_NAME.connor.pile.target.rev.snv|perl -ne '@l=split("\t"); $varinat="$l[0]"."_"."$l[1]"."_"."$l[2]"."_"."$l[3]"; print"$varinat "' `
do
python $SRC/bin/pos_info.snv.py $OUT/$FILE_NAME.new.barcode.sort. $variant >> $OUT/$FILE_NAME.merge_snv_candidate.all.txt
done

sort -k1,1 -k2n,2 -k4,4 -k13,13 $OUT/$FILE_NAME.merge_snv_candidate.all.txt > $OUT/$FILE_NAME.merge_snv_candidate.all.sort.txt

rm $OUT/$FILE_NAME.merge_snv_candidate.all.txt

python $SRC/bin/get_var.py $OUT/$FILE_NAME.merge_snv_candidate.all.sort.txt > $OUT/$FILE_NAME.merge_snv_candidate.var.txt

python $SRC/bin/filter_snv.py $OUT/$FILE_NAME.merge_snv_candidate.var.txt > $OUT/$FILE_NAME.merge_snv_candidate.var.filter.txt

python $SRC/bin/delete_dup.snv.py $OUT/$FILE_NAME.merge_snv_candidate.var.filter.txt > $OUT/$FILE_NAME.final_snv_candidate.pos.txt

python $SRC/bin/filter_fam_num.py $OUT/$FILE_NAME.final_snv_candidate.pos.txt $NUM_SNV $MIN_DEPTH > $OUT/$FILE_NAME.final_snv_candidate.over_threshold.txt

python $SRC/bin/check_barcode.py $OUT/$FILE_NAME.final_snv_candidate.over_threshold.txt $OUT/$FILE_NAME.merge_snv_candidate.var.filter.txt > $OUT/$FILE_NAME.exclude_candidate.snv.txt

python $SRC/bin/strand_bias_calc_1.py $OUT/$FILE_NAME.connor.pile $OUT/$FILE_NAME.final_snv_candidate.over_threshold.txt > $OUT/$FILE_NAME.final_snv_candidate.strand_bias.txt

python $SRC/bin/strand_bias_calc_2.py $OUT/$FILE_NAME.final_snv_candidate.strand_bias.txt > $OUT/$FILE_NAME.final_snv_candidate.strand_bias.p_value.txt

rm $OUT/$FILE_NAME.final_snv_candidate.strand_bias.txt

python $SRC/bin/final_call.py $OUT/$FILE_NAME.exclude_candidate.snv.txt $OUT/$FILE_NAME.final_snv_candidate.strand_bias.p_value.txt $OUT/$FILE_NAME.final_snv_candidate.over_threshold.txt|python $SRC/bin/vcf.py /dev/stdin > $OUT/$FILE_NAME.eVIDENCE.snv.vcf

rm $OUT/$FILE_NAME.exclude_candidate.snv.txt
rm $OUT/$FILE_NAME.final_snv_candidate.strand_bias.p_value.txt
rm $OUT/$FILE_NAME.final_snv_candidate.over_threshold.txt
rm $OUT/$FILE_NAME.merge_snv_candidate.var.filter.txt
rm $OUT/$FILE_NAME.merge_snv_candidate.var.txt
rm $OUT/$FILE_NAME.merge_snv_candidate.all.sort.txt
rm $OUT/$FILE_NAME.new.barcode.sort.*
rm $OUT/$FILE_NAME.connor.pile.target.rev.snv
rm $OUT/$FILE_NAME.connor.pile

for variant in `cat $OUT/$FILE_NAME.connor.pile.target.rev.indel|perl -ne '@l=split("\t"); $varinat="$l[0]"."_"."$l[1]"."_"."$l[2]"."_"."$l[3]"; print"$varinat "' `
do
python $SRC/bin/pos_info.indel.py $OUT/$FILE_NAME.new.barcode.sort. $variant >> $OUT/$FILE_NAME.merge_indel_candidate.all.txt
done

sort -k1,1 -k2n,2 -k4,4 -k13,13 $OUT/$FILE_NAME.merge_indel_candidate.all.txt > $OUT/$FILE_NAME.merge_indel_candidate.all.sort.txt

rm $OUT/$FILE_NAME.merge_indel_candidate.all.txt

python $SRC/bin/get_var.py $OUT/$FILE_NAME.merge_indel_candidate.all.sort.txt > $OUT/$FILE_NAME.merge_indel_candidate.var.txt

python $SRC/bin/filter_indel.py $OUT/$FILE_NAME.merge_indel_candidate.var.txt > $OUT/$FILE_NAME.merge_indel_candidate.var.filter.txt

python $SRC/bin/delete_dup.indel.py $OUT/$FILE_NAME.merge_indel_candidate.var.filter.txt > $OUT/$FILE_NAME.final_indel_candidate.pos.txt

python $SRC/bin/filter_fam_num.py $OUT/$FILE_NAME.final_indel_candidate.pos.txt $NUM_INDEL $MIN_DEPTH > $OUT/$FILE_NAME.final_indel_candidate.over_threshold.txt

python $SRC/bin/check_barcode.py $OUT/$FILE_NAME.final_indel_candidate.over_threshold.txt $OUT/$FILE_NAME.merge_indel_candidate.var.filter.txt > $OUT/$FILE_NAME.exclude_candidate.indel.txt

python $SRC/bin/final_call.py $OUT/$FILE_NAME.exclude_candidate.indel.txt $OUT/$FILE_NAME.final_indel_candidate.over_threshold.txt|python $SRC/bin/vcf.py /dev/stdin > $OUT/$FILE_NAME.eVIDENCE.indel.vcf

rm $OUT/$FILE_NAME.exclude_candidate.indel.txt
rm $OUT/$FILE_NAME.final_indel_candidate.over_threshold.txt
rm $OUT/$FILE_NAME.merge_indel_candidate.var.filter.txt
rm $OUT/$FILE_NAME.merge_indel_candidate.var.txt
rm $OUT/$FILE_NAME.merge_indel_candidate.all.sort.txt
rm $OUT/$FILE_NAME.new.barcode.sort.*
rm $OUT/$FILE_NAME.connor.pile.target.rev.indel

