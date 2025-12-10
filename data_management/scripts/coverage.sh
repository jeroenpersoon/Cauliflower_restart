#!/bin/bash
echo "Liria:"
samtools depth -a liria_f1_sorted.bam | awk '{sum+=$3} END { print "Gemiddelde coverage =", sum/NR }'
echo "caniego:"
samtools depth -a caniego_F1_sorted.bam | awk '{sum+=$3} END { print "Gemiddelde coverage =", sum/NR }'
echo "TKI-0143:"
samtools depth -a TKI-0143_sorted.bam | awk '{sum+=$3} END { print "Gemiddelde coverage =", sum/NR }'
echo "TKI-0155:"
samtools depth -a TKI-0155_sorted.bam | awk '{sum+=$3} END { print "Gemiddelde coverage =", sum/NR }'
