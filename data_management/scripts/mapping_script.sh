bwa mem -t 16 T22.chr.filtered.fna ../caniego_F1_R1.fq ../caniego_F1_R2.fq > caniego_F1.sam
bwa mem -t 16 T22.chr.filtered.fna ../TKI-0143_R1_001.fastq ../TKI-0143_R2_001.fastq > TKI-0143.sam
bwa mem -t 16 T22.chr.filtered.fna ../TKI-0155_R1_001.fastq ../TKI-0155_R2_001.fastq > TKI-0155.sam

samtools sort caniego_F1.sam > caniego_F1_sorted.bam
samtools sort TKI-0143.sam > TKI-0143_sorted.bam
samtools sort TKI-0155.sam > TKI-0155_sorted.bam

samtools index caniego_F1_sorted.bam
samtools index TKI-0143_sorted.bam
samtools index TKI-0155_sorted.bam

nice freebayes -f T22.chr.filtered.fna liria_f1_sorted.bam caniego_F1_sorted.bam TKI-0143_sorted.bam TKI-0155_sorted.bam > cauliflower_reseq_4_freeb.vcf
