# AllofUs
Repository for the scripts related to the All of Us dataset v8 normalization and annoataions for exome datasets chromosomes 1-22. All steps are performed on the All of Us Analysis Workbench: https://workbench.researchallofus.org/ 

## Order of operations for file usage
1. Normalization
   -exome_vcf_file_map.py
   -split_multiallelic_dsub.ipynb
2. Annotation
   -Dockerfile (optional if you need to create your own image)
   -AoU_annotations.ipynb

BIG NOTE: The files (plugins) used for annotating are all available though ensembl VEP download: https://useast.ensembl.org/info/docs/tools/vep/script/vep_plugins.html

LOFTEE is the only third party plugin with all files necessary here:
https://github.com/konradjk/loftee/tree/grch38


# General information about normalization and annotation set up
Below is the pathway to view and use interval vcf chromosome files. These files use the UCSC BED file to list the chromosomes and positions

`gsutil -u $GOOGLE_PROJECT ls gs://fc-aou-datasets-controlled/v8/wgs/short_read/snpindel/exome/vcf/`

We looked at the .interval_list files and referenced them looking at the HD (Header) Lines:
These lines (starting with “@HD”) contain global metadata about the file, such as the SAM version and sort order.

Sequence (SQ) Lines:
Each SQ line defines a reference sequence with its name, full length, and additional metadata. This should repeat in every  `.interval_list` file like the HD lines with all the chromosomes. I just pulled this one as an example.

`@SQ     SN:chr21        LN:46709983     M5:974dc7aec0b755b19f031418fdedf293     AS:38`   `UR:/seq/references/Homo_sapiens_assembly38/v0/Homo_sapiens_assembly38.fasta     SP:Homo sapiens`

Interval (Alignment) Line:
These lines follow the header and specify the genomic intervals (or alignments) on a given reference. They are at the 
bottom of the file and the coordinates being used for a given vcf file.

`chrX    134992201       134992488       +       .`

The interval lines can be multiple lines. If you type: `gsutil -u $GOOGLE_PROJECT cat gs://fc-aou-datasets-controlled/v8/wgs/short_read/snpindel/exome/vcf/0000020007.interval_list | tail -n 30`

You will see the below example

`chrX    156024119       156024287       +       .`

`chrX    156025017       156025084       +       .`

 
Once mapped the intervaled files were merged together to their appropriate chr# file. The individual mapped files can be found in my workspace bucket:
`gs://fc-secure-5e490ca2-d5ae-40a3-aa5e-7355e31ab9cc/newID_VCF`
Merged and compressed vcf files used to run in VEP are here

`gs://fc-secure-5e490ca2-d5ae-40a3-aa5e-7355e31ab9cc/chr_newID`

## Build the Docker Container and push the Image

To simplify the process we built a docker container that had samtools included and the other dependencies to run a dsub job in the virtual machine environment since the run times are taking awhile. This will help run things in the background more smoothly. If you ever need to build a container with bigwig file dependencies just copy and build the Dockerfile and push it to the gc google cloud. It will take the latest version of VEP and add everything else needed to run your command.

## Biofilter VEP Plugin Resources (README)

# Biofilter VEP Plugin Resources

Repository section for the **VEP plugin setup** used to modernize Biofilter with updated annotation methods:  
**LOFTEE**, **CADD**, **dbNSFP**, **SpliceAI**, and **AlphaMissense**.  

These plugins provide AI- and evidence-based functional annotations for coding, splicing, and regulatory variants.

All plugins except **LOFTEE** can be installed via the Ensembl VEP plugin manager:  
🔗 [https://useast.ensembl.org/info/docs/tools/vep/script/vep_plugins.html](https://useast.ensembl.org/info/docs/tools/vep/script/vep_plugins.html)

LOFTEE (Loss-Of-Function Transcript Effect Estimator) is a third-party plugin with required files here:  
🔗 [https://github.com/konradjk/loftee/tree/grch38](https://github.com/konradjk/loftee/tree/grch38)

---

## ✅ Required Plugin Files

### 🧩 LOFTEE (LoF plugin)

| File / Path | Description |
|--------------|-------------|
| `${PLUGIN_DIR}/loftee/` | LOFTEE plugin directory (from VEP_plugins) |
| `${HUMAN_ANCESTOR_FILE}` → `human_ancestor.fa.gz` | Human ancestor FASTA |
| `${HUMAN_ANCESTOR_INDEX}` → `human_ancestor.fa.gz.fai` | FASTA index |
| `${CONSERVATION_FILE}` | LOFTEE conservation reference |
| `${GERP_FILE_PATH}` | GERP++ BigWig file for conservation |

> **Note:** Use the plugin name `LoF` and specify these files via `loftee_path:`, `human_ancestor_fa:`, etc.

---

### ⚙️ CADD

| File / Path | Description |
|--------------|-------------|
| `${PLUGIN_DIR}/CADD/whole_genome_SNVs_inclAnno.tsv.gz` | SNV CADD scores |
| `${PLUGIN_DIR}/CADD/whole_genome_SNVs_inclAnno.tsv.gz.tbi` | Tabix index for SNVs |
| `${PLUGIN_DIR}/CADD/whole_genome_InDels_inclAnno.tsv.gz` | Indel CADD scores |
| `${PLUGIN_DIR}/CADD/whole_genome_InDels_inclAnno.tsv.gz.tbi` | Tabix index for Indels |

---

### 🧬 dbNSFP

| File / Path | Description |
|--------------|-------------|
| `${PLUGIN_DIR}/dbNSFP/dbNSFP4.9a_grch38.gz` | dbNSFP variant prediction database (GRCh38) |
| `${PLUGIN_DIR}/dbNSFP/dbNSFP4.9a_grch38.gz.tbi` | Tabix index for dbNSFP |

**Example fields:**  
`Ensembl_transcriptid, Uniprot_acc, VEP_canonical, LRT_pred, SIFT_pred, MutationTaster_pred, Polyphen2_HDIV_pred, Polyphen2_HVAR_pred, REVEL_score`

---

### 🧠 SpliceAI

| File / Path | Description |
|--------------|-------------|
| `${PLUGIN_DIR}/SpliceAI/spliceai_scores.raw.snv.hg38.vcf.gz` | Precomputed SNV splice predictions |
| `${PLUGIN_DIR}/SpliceAI/spliceai_scores.raw.snv.hg38.vcf.gz.tbi` | Tabix index for SNV file |
| `${PLUGIN_DIR}/SpliceAI/spliceai_scores.raw.indel.hg38.vcf.gz` | Precomputed Indel splice predictions |
| `${PLUGIN_DIR}/SpliceAI/spliceai_scores.raw.indel.hg38.vcf.gz.tbi` | Tabix index for Indel file |

---

### 🧠 AlphaMissense

| File / Path | Description |
|--------------|-------------|
| `${PLUGIN_DIR}/AlphaMissense/AlphaMissense_hg38.tsv.gz` | AlphaMissense precomputed pathogenicity scores |
| `${PLUGIN_DIR}/AlphaMissense/AlphaMissense_hg38.tsv.gz.tbi` | Tabix index (`tabix -s 1 -b 2 -e 2`) |

> **Note:** Plugin name is `AlphaMissense`; specify via  
> `file=${PLUGIN_DIR}/AlphaMissense/AlphaMissense_hg38.tsv.gz`

---

### 📚 Reference & Cache Files

| File / Path | Description |
|--------------|-------------|
| `${EXTRACTED_CACHE_DIR}` | VEP cache directory (offline mode) |
| `${PLUGIN_DIR}/Homo_sapiens_assembly38.fasta` | Reference FASTA (GRCh38) |
| `${PLUGIN_DIR}/Homo_sapiens_assembly38.fasta.fai` | FASTA index |
| `${PLUGIN_DIR}` | Plugin directory specified with `--dir_plugins` |

---

## 📁 Example Directory Layout

```bash
${PLUGIN_DIR}/
  loftee/
  CADD/
    whole_genome_SNVs_inclAnno.tsv.gz
    whole_genome_SNVs_inclAnno.tsv.gz.tbi
    whole_genome_InDels_inclAnno.tsv.gz
    whole_genome_InDels_inclAnno.tsv.gz.tbi
  dbNSFP/
    dbNSFP4.9a_grch38.gz
    dbNSFP4.9a_grch38.gz.tbi
  SpliceAI/
    spliceai_scores.raw.snv.hg38.vcf.gz
    spliceai_scores.raw.snv.hg38.vcf.gz.tbi
    spliceai_scores.raw.indel.hg38.vcf.gz
    spliceai_scores.raw.indel.hg38.vcf.gz.tbi
  AlphaMissense/
    AlphaMissense_hg38.tsv.gz
    AlphaMissense_hg38.tsv.gz.tbi
  Homo_sapiens_assembly38.fasta
  Homo_sapiens_assembly38.fasta.fai
