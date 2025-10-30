#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=8
#SBATCH --time=1:00:00
#SBATCH --mail-user=bcorwin@uoregon.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=dedup
#SBATCH --output=logs/dedup_%j.out
#SBATCH --error=logs/dedup_%j.err

/usr/bin/time -v ./corwin_deduper.py -f C1_SE_uniqAlign.sorted.sam -o dedup.sam -u STL96.txt

exit