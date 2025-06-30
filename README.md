# AllofUs
Repository for the scripts related to the All of Us dataset v8 normalization and annoataions for exome datasets chromosomes 1-22. All steps are performed on the All of US Analysis Workbench: https://workbench.researchallofus.org/ 

BIG NOTE: The files used for annotating are all available though ensembl VEP download: https://useast.ensembl.org/info/docs/tools/vep/script/vep_plugins.html

LOFTEE is the only third party plugin with all files necessary here:
https://github.com/konradjk/loftee/tree/grch38


#General Information about normalization and annotation
Below is the pathway to view and use interval vcf chromosome files. These files use the UCSC BED file to list the chromosomes and positions

gsutil -u $GOOGLE_PROJECT ls gs://fc-aou-datasets-controlled/v8/wgs/short_read/snpindel/exome/vcf/

We looked at the .interval_list files and referenced them looking at the HD (Header) Lines:
These lines (starting with “@HD”) contain global metadata about the file, such as the SAM version and sort order.

Sequence (SQ) Lines:
Each SQ line defines a reference sequence with its name, full length, and additional metadata. This should repeat in every  .interval_list file like the HD lines with all the chromosomes. I just pulled this one as an example.
@SQ     SN:chr21        LN:46709983     M5:974dc7aec0b755b19f031418fdedf293     AS:38   UR:/seq/references/Homo_sapiens_assembly38/v0/Homo_sapiens_assembly38.fasta     SP:Homo sapiens

Interval (Alignment) Line:
These lines follow the header and specify the genomic intervals (or alignments) on a given reference. They are at the bottom of the file and the coordinates being used for a given vcf file.
chrX    134992201       134992488       +       .The interval lines can be multiple lines. If you type gsutil -u $GOOGLE_PROJECT cat gs://fc-aou-datasets-controlled/v8/wgs/short_read/snpindel/exome/vcf/0000020007.interval_list | tail -n 30

You will see the below example
chrX    156024119       156024287       +       .
chrX    156025017       156025084       +       .

 

Once mapped the intervaled files were merged together to their appropriate chr# file. The individual mapped files can be found in my workspace bucket
gs://fc-secure-5e490ca2-d5ae-40a3-aa5e-7355e31ab9cc/newID_VCF
Merged and compressed vcf files used to run in VEP are here

gs://fc-secure-5e490ca2-d5ae-40a3-aa5e-7355e31ab9cc/chr_newID

## Build the Docker Container and push the Image

To simplify the process we built a docker container that had samtools included and the other dependencies to run a dsub job in the virtual machine environment since the run times are taking awhile. This will help run things in the background more smoothly. If you ever need to build a container with bigwig file dependencies just copy and build the Dockerfile and push it to the gc google cloud. It will take the latest version of VEP and add everything else needed to run your command.
