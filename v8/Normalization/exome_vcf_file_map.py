# load python packages
import subprocess
import argparse as ap
from pathlib import Path

# add arguments
def make_arg_parser():
    parser = ap.ArgumentParser(description=".")

    parser.add_argument('--input', required=True)

    parser.add_argument('--file_number', required=True)
    
    parser.add_argument('--output_dir', required=True)

    return parser

args = make_arg_parser().parse_args()

# parse arguments
input_filepath = args.input
file_number=args.file_number
output_dir=args.output_dir

# extract filename from input file path
input_filename=Path(input_filepath).name

# write command
command = (f'echo {input_filename} > {file_number}.filename.txt &&'
           f'zcat {input_filepath} | grep -v "#" | head -n1 | cut -f1-2 > {file_number}.start.txt &&'
           f'zcat {input_filepath} | tail -n1 | cut -f1-2 > {file_number}.stop.txt &&'
           f'paste -d "\t" {file_number}.filename.txt {file_number}.start.txt {file_number}.stop.txt > {file_number}.exome_map.txt &&'
           f'cp {file_number}.exome_map.txt {output_dir}'
          )

# run command
subprocess.run(command, text=True, shell=True)
