# LRPHASE FUNCTIONALITY NOTES:
```
input_data = InputData(output_directory_path=output_directory_path) # Create an instance of the InputData class to handle all of the input file reparation/validation/metadata/etc. 

input_data.add_haplotype_information('HG001.vcf.gz') # load in a vcf file with haplotype information

input_data.add_reads('alignment_sorted.bam',sample='HG001',reference_genome='reference_sequences/hg38_autosomal.fa') # load in the long reads to be phased and their sample name 

for phasable_sample in input_data:  # iterating over an object of the InputData class returns objects of the PhasableSample class: one for each sample hat is found in both the VCF file and the READ data.
    print(phasable_sample.sample)   # prints the sample name "HG001"
    
    for alignment in phasable_sample: # iterating over an object of the PhasableSample class returns objects of the pysam.AlignedSegment class: one for each alignment in the input data that belongs to a specific sample.
    
          phased_read=PhasedRead(alignment, phasable_sample) # then you can phase each alignment using the PhasedRead class
          print(phased_read,phased_read.phase) # extract whatever info you are looking for (there are 50+ propertiesoded for this class, see the @property decorated functions under the PhasedRead class)
```

A simple phasing pipeline would look like this:
```
input_data = InputData(output_directory_path)
input_data.add_haplotype_information(vcf_file_path)
input_data.add_reads('hg001_alignment_sorted.bam',sample='HG001')
for phasable_sample in input_data:
    print(phasable_sample.sample)
    for alignment in phasable_sample:
        phased_read=PhasedRead(alignment, phasable_sample)
        if phased_read.is_Phased:
            print(phased_read, phased_read.phase)
            phased_read.write_to_bam()
```
## The simulation process:
### 1. Create a custom reference sequence:
####    a. can specify regions from a fasta, autosomal, etc
####    b. can specify one of haplotypes and a haplotype vcf file, and then generate those specific haplotype sequences (you must also provide the                  reference sequence that the vcf is based off of)
### 2. Generate (millions) reads from a given set of reference sequences (like only the paternal chromosomes of GM12878) and automatically send them            through a phasing pipeline.

#### Each read will be evaluated for its alignment accuracy (because pbsim2 records where it genereated the read from in the ref) and also whether the        phasing was correct (because the read came from one specific haplotype)

#### The reads can be generated using various custom error profiles/lengths/mutations preferences/etc or you can provide a fastq file and it will pick        these parameters so that the simuated reads mimic the characteristics of the reads in the fastq file.

#### So this is how we are going to generated the calibration plot of our phasing statistic: we will fit a curve of the phasing error vs                      log_likelihood_ratio. It's a power law relationship, so we used the powlaw package to automate the fitting process.

## Example simulation code:
### Notes: if you pass InputData a url for any of the data it will download it and parse/validate it as usual. I included a bunch of reference urls in       the urls.py file that can be accessed by importing: (from LRphase import urls). There are two dictionaries (access them by: urls.hg38 or urls.hg19)     for the hg38 and hg19 versions of the human reference genome
```
from LRphase import urls
from LRphase import InputData
from LRphase import SimulatePhasedData
from LRphase import PhasedRead

output_directory = '/home/LRphase'
sample='HG001'
assembly_version=urls.hg38
hg38_reference_sequence_url = urls.hg38['reference_sequence']
HG001_vcf_url = urls.hg38['HG001']
input_data = InputData.InputData(output_directory_path=output_directory)
hg38_reference_sequence_path = input_data.add_reference_sequence(hg38_reference_sequence_url, output_directory = output_directory+'/reference_genome/')
vcf_file_path = input_data.add_haplotype_information('HG001_vcf_url',ignore_phase_sets=False)
autosomal_hg38_ref_seq_path = SimulatePhasedData.create_fasta_file(input_fasta_file_path = hg38_reference_sequence_path, output_fasta_file_path =  output_directory+'/reference_genome/autosomal_hg38_ref.fa', only_autosomal: True)
haplotype_specific_fasta = SimulatePhasedData.generate_haplotype_specific_fasta('1','HG001',autosomal_hg38_ref_seq_path,vcf_file_path,output_reference_sequence_path= output_directory+'/reference_genome/autosomal_hg38_ref_HG001_hap1_.fa',chain_file_path=output_directory+'/reference_genome/autosomal_hg38_ref_HG001_hap1_.chain')
simulated_fastq = SimulatePhasedData.simulate_reads_pbsim2(
        reference_sequence = haplotype_specific_fasta, depth = 25,
        simulation_mode = 'pbsim2/data/R103.model',
        difference_ratio = '23:31:46', length_mean = 25000,
        length_max = 1000000, length_min = 100,
        length_sd = 20000, accuracy_min = 0.01,
        accuracy_max = 1.00, accuracy_mean = 0.80,
        output_directory = output_directory+'/simulated_reads/', sample = 'HG001',
        haplotype = '1')
input_data.add_reads(simulated_fastq,sample='HG001',reference_genome=hg38_reference_sequence_path)
for phasable_sample in input_data:
    if phasable_sample.sample == 'HG001':
        for alignment in phasable_sample:
            phased_read = PhasedRead.PhasedRead(alignment, phasable_sample) # intended functionality of classes, but explicit input is also ok:
            #phased_read = PhasedRead.PhasedRead(alignment, vcf_file = phasable_sample.vcf_file_path, sample = 'HG001', evaluate_true_alignment = True)
            print(phased_read)
            print(phased_read.matches_true_alignment)
            print(phased_read.phase, phased_read.is_phased_correctly, phased_read.log_likelihood_ratio)
```
# PyPI:

pip install LRphase

This will install the current PyPI (https://pypi.org/project/LRphase/) build as a command line tool and as a python library that you can import and use to build phasing pipelines.

# INSTALLATION NOTES:
```
#Install simulation/alignment tools (pbsim2, minimap2, paftools.js)
rm -r minimap2/
git clone https://github.com/lh3/minimap2
cd minimap2 && make
install -p minimap2/minimap2 /usr/local/bin

rm -r paftools
mkdir paftools
cd paftools && curl -L https://github.com/attractivechaos/k8/releases/download/v0.2.4/k8-0.2.4.tar.bz2 | tar -jxf -
cd paftools && cp k8-0.2.4/k8-`uname -s` k8
cd paftools && install -p k8 /usr/local/bin
install -p minimap2/misc/paftools.js /usr/local/bin

rm -r pbsim2
git clone https://github.com/yukiteruono/pbsim2
cd pbsim2/ && ./configure && make && make install

#Install python packages
pip install pysam biopython numpy pyliftover

#Install HTSlib tools (samtools, bgzip, bcftools, tabix)
apt install tabix bcftools samtools
```
# GREG UPLOAD NOTES:
```
rm -r LRphase_env/
python3 -m venv LRphase_env
source LRphase_env/bin/activate
rm -rf build
rm -rf src/*.egg-info
python3 -m pip install --upgrade pip setuptools wheel pysam pyliftover biopython twine build
python3 setup.py clean --all sdist bdist_wheel
twine upload --skip-existing dist/*tar.gz
pip install LRphase
```
# reference genome notes:
https://lh3.github.io/2017/11/13/which-human-reference-genome-to-use

Consider adopting the OpenAPI web framework- sequence repo:
https://github.com/biocommons/seqrepo-rest-service
https://github.com/biocommons/biocommons.seqrepo/
https://github.com/biocommons/bioutils

# LRphase
A tool for phasing individual reads when haplotype information is available. 
* Main functions: (1) Assigns phase to individual reads and (2) provides an estimate of phasing quality (phred-scaled phasing error rate)
* Recommended Usage: (1) Phasing low coverage read data, (2) phasing noisy long-read data generated by nanopore sequencing, and (3) tagging or filtering reads according to phase, phasing quality, phase_set, and/or sample.

## Requirements

Full Requirements: 
* Python version 3.7 or higher and the numpy, matplotlib, scipy, pysam, and PyVCF Python packages. (Minimap2, samtools, bgzip, and tabix must be installed and added to PATH for full functionality)
```
conda create --name LRphase -c conda-forge python=3.7 pysam numpy matplotlib scipy pyvcf
conda activate LRphase
```
Minimum Requirements (phasing only): 
* The phasing module requires python version 3.7 or higher and the numpy, pysam, and PyVCF Python packages. 

## Installation

pysam installation: https://pysam.readthedocs.io/en/latest/installation.html#installation
conda config --add channels r
conda config --add channels bioconda
conda install pysam

From github
```
git clone https://github.com/castrocp/LRphase
cd LRphase/
python3.7 -m pip install -e .
```
From PyPI
```
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps LRphase-gregfar
```
From conda
```
conda install LRphase
```
# LRphase phasing mode

## Input File Requirements

(1) Haplotype information:
* phased VCF file: must be bgzipped (.vcf.gz) and have a tabix index in same folder (.vcf.gz.tbi). If a .vcf file is provided but it is not bgzipped or indexed, LRphase will convert it to the correct format. (tabix and bgzip must be installed and available on the user's PATH for conversion)
          
(2) Long Reads that orginated from the genomic DNA of cells specific to the VCF file must be provided in one of two formats:
* Unaligned: FASTQ long read file (.fastq or .fastq.gz) and reference genome FASTA file. (minimap2 required on PATH for this option)
  OR
* Aligned: Alignment files in sorted BAM (.sorted.bam) format with an INDEX in same folder (.sorted.bam.bai). If a SAM or unsorted BAM or unindexed BAM alignment file is provided as input, LRphase will convert it to the proper format. 

## Output files
All LRphase options will produce at least two files: a text file with a summary of the run and a table of summary statistics for each read processed. If pysam is available LRphase will distribute the reads from the input BAM file into 4 separate BAM files based on their phasing assignment. (paternal_reads.bam, maternal_reads.bam, unphased_reads.bam, and nonphasable_reads.bam)
