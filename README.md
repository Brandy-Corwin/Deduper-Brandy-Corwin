# Deduper

The script corwin_deduper.py produces a new SAM file without any PCR duplicates. The script assumes a sorted SAM file. To run the script, use the command ```./corwin_deduper.py -f {input sam file} -o {output file} -u {UMI file}```.

You can also run the script by running ```sbatch run_pyscript.sh``` which will run if you have the needed files. This will give you information about runtime of the script and save all printed out information into the .out file in the logs directory.