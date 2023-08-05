# coding=utf-8
import os
import random
import subprocess
import time
from collections import defaultdict
from datetime import date
from shutil import copyfileobj
from typing import List, Optional, Tuple, Union, Any

import pysam
import requests
from pysam import VariantFile, FastaFile

from LRphase import PhasableSample


def _sort_vcf_file(vcf_file_input: object, vcf_file_output: object = None) -> object:
    """

    Args:
        vcf_file_input: Location of VCF file (absolute path)
        vcf_file_output: Location/name of VCF.bgz output (absolute path)

    Returns path to sorted/bgzipped output file.
    """
    if vcf_file_output is None:
        vcf_file_output = vcf_file_input + '.bgz'

    try:
        subprocess.run(
            ["grep -v ^'#' %s | sort -k1,1 -k2,2n | bgzip > %s" % (vcf_file_input, vcf_file_output)],
            check=True, shell=True
        )
        return vcf_file_output
    except Exception as e:
        print(
            "Error occurred when bgzip was run. Bgzip must be installed on PATH for LRphase to "
            "continue. Please check bgzip installation or provide a bgzip compressed vcf file using "
            "the -v option (EX: -v path/to/GM12878.vcf.gz). Error: %s" % e
        )
        return


def _prepare_output_directory(output_directory_path: str) -> Optional[str]:  # Optional[str]:
    """

    Args:
        output_directory_path (object): 

    Returns:
        Optional[str]:
    """
    print('############## Preparing output_directory ##############')
    if os.path.isfile(output_directory_path):
        print(
            f'Output directory exists as a file. Use -o to specify the name to be given to the output folder. May '
            f'also provide a relative path with a name to create output directory in a different location (EX: -o '
            f'path/to/name). Do not specify a file. '
        )
        return
    elif os.path.exists(output_directory_path):
        print(
            '%s already exists, WARNING: New results will overwrite old files' % os.path.abspath(
                output_directory_path
            ), '\n'
        )
    elif not os.path.exists(output_directory_path):
        os.mkdir(output_directory_path)
        print(f"%s created" % os.path.abspath(output_directory_path), '\n')
    output_directory = os.path.abspath(output_directory_path)
    return output_directory


def _prepare_summary_file(output_directory):
    print('############## Preparing summary_file ##############')

    summary_file_path = os.path.abspath('%s/%s' % (output_directory, 'summary.txt'))
    if os.path.exists(summary_file_path):
        print(
            '%s already exists, WARNING: New results will overwrite old files' % os.path.abspath(summary_file_path),
            '\n'
        )
    elif not os.path.exists(summary_file_path):
        print('%s created' % os.path.abspath(summary_file_path), '\n')
    summary_file = open(summary_file_path, 'w')
    summary_file.write('Start date: %s\n' % str(date.today()))
    start_time = time.time()
    print('%s created' % summary_file_path, '\n')

    return summary_file_path


def _pair_sample_with_vcf(sample, sample_to_vcf_file_dict, ignore_phase_sets):
    if str(sample) in sample_to_vcf_file_dict.keys():
        for vcf_file_path in sample_to_vcf_file_dict[str(sample)].items():
            if ignore_phase_sets:
                return vcf_file_path[0], True
            else:
                return vcf_file_path[0], vcf_file_path[1]
    else:
        return


def _sample_to_alignment_files(sample_to_vcf_file_dict: dict, RG_ID_dict: dict) -> object:
    """
    Create a dictionary relating sample names to alignment files.

    Returns:
        object:
    """
    sample_to_alignment_files = {}
    for sample in sample_to_vcf_file_dict:
        sample_to_alignment_files[sample] = {}
        for file in RG_ID_dict.keys():
            if len([file for key in RG_ID_dict[file].keys() if RG_ID_dict[file][key]['SM'] == sample]) > 0:
                for pair in [{
                    alignment_file_path: any(
                        [RG_ID_dict[alignment_file_path][ID]['RG_tags'] for ID in
                         RG_ID_dict[alignment_file_path].keys()]
                    )
                } for alignment_file_path in RG_ID_dict.keys() if any(
                    [RG_ID_dict[alignment_file_path][ID]['SM'] == sample for ID in
                     RG_ID_dict[alignment_file_path].keys()]
                )]:
                    sample_to_alignment_files[sample][list(pair.keys())[0]] = list(pair.values())[0]
    return sample_to_alignment_files


def _align_long_reads_fastq(long_reads_fastq_path, reference_sequence_input, output_directory):
    """
    Align specified reads file to reference genome via minimap2.
    """
    if not reference_sequence_input:
        print('no reference genome was provided for', long_reads_fastq_path, '. This file will be skipped.')
        return

    print('################ Beginning Sequence Alignment ################')

    start_process_time = time.time()
    reference_sequence_input_path = os.path.abspath(reference_sequence_input)
    if str(long_reads_fastq_path).lower().endswith('.fastq'):
        sam_alignment_path = os.path.abspath(
            '%s/%s%s' % (
                output_directory, os.path.splitext(os.path.basename(long_reads_fastq_path))[0],
                '_alignment.sam')
        )
    elif str(long_reads_fastq_path).lower().endswith('fastq.gz'):
        sam_alignment_path = os.path.abspath(
            '%s/%s%s' % (
                output_directory,
                os.path.splitext(os.path.splitext(os.path.basename(long_reads_fastq_path))[0])[0],
                '_alignment.sam')
        )

    # if subprocess.getstatusoutput(['minimap2 -ax map-ont'+'
    # /home/ubuntu/testing_LRphase/simtest6/reference_sequences/hg38/hg38output_regions_only_autosomal.fa '+
    # '/home/ubuntu/testing_LRphase/simtest6/simulated_reads/hg38output_regions_only_autosomal_hap1_HG001.fastq '+'-o
    # '+'a.sam'])[0] != 0: print('minimap2 failed to run. Installing minimap2 from source...') import getpass
    # password = getpass.getpass() os.system('echo %s | %s' % (password, "sudo -S rm -r minimap2")) subprocess.run([
    # 'git','clone','https://github.com/lh3/minimap2']) os.chdir('minimap2/') subprocess.run('make') os.system('echo
    # %s | %s' % (password, "sudo -S install -p minimap2/minimap2 /usr/local/bin"))
    subprocess.run(
        ['minimap2', '-ax', 'map-ont', '-Y', '-L', '--secondary=no', '--MD', reference_sequence_input_path,
         long_reads_fastq_path, '-o', sam_alignment_path], check=True
    )

    # try:

    # # '-R', '@RG\\tID:'+str(ID)+'\\tSM:'+str(sample)+'\\tDS:'+str(sample_description), '-a' = creates aligned
    # # SAM file '-x' to choose a preset (map-ont in this case): 'map-ont' Slightly more sensitive for Oxford
    # # Nanopore to reference mapping (-k15). For PacBio reads, HPC minimizers consistently leads to faster
    # # performance and more sensitive results in comparison to normal minimizers. For Oxford Nanopore data,
    # # normal minimizers are better, though not much. The effectiveness of HPC is determined by the sequencing
    # # error mode. '-L' option is used when working with ultra-long nanopore reads to account for CIGAR
    # # strings > 65,535 characters '--secondary=no' Do not output secondary alignments '--MD' Output the MD
    # # tag (see the SAM spec). '-R', '@RG\\tID:'str(ID)'\\tSM:'str(sample)'\\tDS:'str(sample_description) Read
    # # group information '-o' FILE Output alignments to FILE [stdout].
    # except Exception as e:
    # print('Error occurred when minimap2 was run. minimap2 must be installed on PATH for LRphase to continue. '
    # 'Please check minimap2 installation or provide an alignment file using the -a option. Error: %s' % e)
    # return

    end_process_time = time.time()
    total_process_time = end_process_time - start_process_time

    print(f'Alignment finished in {total_process_time:.2f} seconds', '\n')

    # summary_file(output_directory, time.time()-start_process_time, inspect.stack()[0][3], sam_alignment_path)

    return sam_alignment_path


def _sort_and_index_alignment_file(long_reads_alignment_path, output_directory: object):
    start_process_time = time.time()

    sorted_bam_file_path = os.path.abspath(
        '%s/%s%s' % (
            output_directory, os.path.splitext(os.path.basename(long_reads_alignment_path))[0],
            '_sorted.bam')
    )
    print('############## Sorting and indexing bam file ##############')
    pysam.sort('-O', 'BAM', long_reads_alignment_path, '-o', sorted_bam_file_path)
    # try: subprocess.run(['samtools sort -O BAM -o %s %s' % ( sorted_bam_file_path, long_reads_alignment_path)],
    # shell=True) # pysam.sort('-l','9','-m','1500M','-@','4','-O', 'BAM', long_reads_alignment_path, '-o',
    # sorted_bam_file_path, catch_stdout=False) except Exception as e: print(e,'Error occurred when using pysam.sort
    # with 8 threads on %s. Trying 0 extra threads now.' % long_reads_alignment_path) subprocess.run(['samtools sort
    # -O BAM -o %s %s' % (sorted_bam_file_path, long_reads_alignment_path)], shell=True) # pysam.sort('-O', 'bam',
    # long_reads_alignment_path, '-o', sorted_bam_file_path, catch_stdout=False)

    print('Created %s' % sorted_bam_file_path)
    pysam.index(sorted_bam_file_path)
    print('Created %s.bai' % sorted_bam_file_path)
    os.remove(long_reads_alignment_path)
    end_process_time = time.time()
    total_process_time = end_process_time - start_process_time

    print(f'Sorting and indexing finished in {total_process_time:.2f} seconds', '\n')
    # summary_file(output_directory, time.time()-start_process_time, inspect.stack()[0][3],
    # [sorted_bam_file_path, 'Created %s.bai' % sorted_bam_file_path])
    return sorted_bam_file_path


def _prepare_alignment(output_directory: str, long_reads_alignment_path: str) -> Union[None, str]:
    """

    Args:
        output_directory:
        long_reads_alignment_path:

    Returns:
        Union[None, str]:

    """
    start_process_time = time.time()
    long_read_file_pysam = pysam.AlignmentFile(long_reads_alignment_path)
    if long_read_file_pysam.format == 'BAM':
        if long_read_file_pysam.has_index():
            sorted_bam_file_path = os.path.abspath(long_reads_alignment_path)
            print('%s is a valid alignment file with an index.' % long_reads_alignment_path)
        elif not long_read_file_pysam.has_index():
            print(
                '%s is a .bam file but the index cannot be found. Sorting and indexing bam file.' % long_reads_alignment_path
            )
            sorted_bam_file_path = _sort_and_index_alignment_file(long_reads_alignment_path, output_directory)
            # subprocess.run(['rm %s' % long_reads_alignment_path],shell=True)
    elif long_read_file_pysam.format == 'SAM':
        print(
            '%s is a .sam file. Converting to binary (.bam), sorting, and indexing bam file.' % long_reads_alignment_path
        )
        sorted_bam_file_path = _sort_and_index_alignment_file(long_reads_alignment_path, output_directory)
        # subprocess.run(['rm %s' % long_reads_alignment_path],shell=True)
    else:
        print(
            "Error: Pysam does not recognize %s as being in SAM or BAM format. If aligned reads are provided as "
            "input they must be in proper .sam or .bam format." % long_reads_alignment_path
        )
        return
        # summary_file(self.output_directory, time.time()-start_process_time, inspect.stack()[0][3],
    # sorted_bam_file_path)
    return sorted_bam_file_path


def _unique_RG_IDs_from_RG_tags(RG_ID_dict: dict, unique_RG_IDs: dict, alignment_file_path: str) -> object:
    """

    Args:
        RG_ID_dict (dict):
        unique_RG_IDs (dict):
        alignment_file_path (str):
    """
    with pysam.AlignmentFile(alignment_file_path, 'rb') as bam_file:
        RG_tags = bam_file.header.get('RG')
    if RG_tags is None:
        RG_ID_dict[str(alignment_file_path)] = 'No RG tags'
    else:
        RG_ID_dict[str(alignment_file_path)] = {}
        for RG_tag in RG_tags:
            RG_ID_dict[str(alignment_file_path)][str(RG_tag['ID'])] = {}
            RG_ID_dict[str(alignment_file_path)][str(RG_tag['ID'])]['DS'] = str(RG_tag['DS'])
            RG_ID_dict[str(alignment_file_path)][str(RG_tag['ID'])]['SM'] = str(RG_tag['SM'])
            RG_ID_dict[str(alignment_file_path)][str(RG_tag['ID'])]['RG_tags'] = True
            if str(RG_tag['ID']) in list(unique_RG_IDs):
                if unique_RG_IDs[str(RG_tag['ID'])]['DS'] == str(RG_tag['DS']) and unique_RG_IDs[str(RG_tag['ID'])][
                    'SM'] == str(RG_tag['SM']):
                    RG_ID_dict[str(alignment_file_path)][str(RG_tag['ID'])]['outputID'] = str(RG_tag['ID'])
                else:
                    not_unique = True
                    i = 0
                    while not_unique:
                        newID: str = str(RG_tag['ID']) + '_' + str(i)
                        if str(newID) not in list(unique_RG_IDs):
                            RG_ID_dict[str(alignment_file_path)][str(RG_tag['ID'])]['outputID'] = str(newID)
                            unique_RG_IDs[str(newID)] = {}
                            unique_RG_IDs[str(newID)]['DS'] = str(RG_tag['DS'])
                            unique_RG_IDs[str(newID)]['SM'] = str(RG_tag['SM'])
                            not_unique = False
                        i += 1
            else:
                RG_ID_dict[str(alignment_file_path)][str(RG_tag['ID'])]['outputID'] = str(RG_tag['ID'])
                unique_RG_IDs[str(RG_tag['ID'])] = {}
                unique_RG_IDs[str(RG_tag['ID'])]['DS'] = str(RG_tag['DS'])
                unique_RG_IDs[str(RG_tag['ID'])]['SM'] = str(RG_tag['SM'])
    return RG_ID_dict, unique_RG_IDs


def _extract_RG_info_from_long_read_input(long_read_input: List[
    str]) -> object:  # tuple[Union[Union[str, bytes], Any], object, Optional[Any], Optional[Any], Optional[Any]]:
    """

    Returns:
        object:
    """
    long_read_input_path = os.path.abspath(long_read_input[0])
    if len(long_read_input) == 1:
        input_ID = None
        input_sample = None
        input_sample_description = None
        input_reference_sequence_input = None
    elif len(long_read_input) == 2:
        input_ID = long_read_input[1]
        input_sample = None
        input_sample_description = None
        input_reference_sequence_input = None
    elif len(long_read_input) == 3:
        input_ID = long_read_input[1]
        input_sample = long_read_input[2]
        input_sample_description = None
        input_reference_sequence_input = None
    elif len(long_read_input) == 4:
        input_ID = long_read_input[1]
        input_sample = long_read_input[2]
        input_sample_description = long_read_input[3]
        input_reference_sequence_input = None
    elif len(long_read_input) >= 5:
        input_ID: object = long_read_input[1]
        input_sample = long_read_input[2]
        input_sample_description = long_read_input[3]
        input_reference_sequence_input = long_read_input[4]
    return long_read_input_path, input_ID, input_sample, input_sample_description, input_reference_sequence_input


def _sample_to_vcf_file_dict(vcf_file_paths):
    """
    Create a dictionary relating sample names to vcf file paths.
    """
    sample_to_vcf_file_dict = {}
    for vcf_file_path in vcf_file_paths:
        vcf_file = pysam.VariantFile(list(vcf_file_path.keys())[0])
        for sample in vcf_file.header.samples:
            sample_to_vcf_file_dict[str(sample)] = vcf_file_path
        vcf_file.close()  # Clean up after ourselves!
    return sample_to_vcf_file_dict


def _compile_read_groups(
        alignment_file_path, sample, ID, sample_description, RG_ID_dict, unique_RG_IDs, ignore_samples
):
    if ignore_samples:
        RG_ID_dict[str(alignment_file_path)] = 'ignore_samples'
    else:
        with pysam.AlignmentFile(alignment_file_path, 'rb') as bam_file:
            RG_tags = bam_file.header.get('RG')
        if sample is not None:
            RG_ID_dict[str(alignment_file_path)] = {}
            if ID is not None:
                RG_ID_dict[str(alignment_file_path)][str(ID)] = {}
                RG_ID_dict[str(alignment_file_path)][str(ID)]['SM'] = str(sample)
                RG_ID_dict[str(alignment_file_path)][str(ID)]['outputID'] = str(ID)
                RG_ID_dict[str(alignment_file_path)][str(ID)]['RG_tags'] = False
                if sample_description is not None:
                    RG_ID_dict[str(alignment_file_path)][str(ID)]['DS'] = str(sample_description)
                else:
                    RG_ID_dict[str(alignment_file_path)][str(ID)]['DS'] = str(
                        'LRphase_input_file_' + str(alignment_file_path)
                    )
            else:
                ID = '0' + str(random.randint(1, 10000))
                RG_ID_dict[str(alignment_file_path)][str(ID)] = {}
                RG_ID_dict[str(alignment_file_path)][str(ID)]['SM'] = str(sample)
                RG_ID_dict[str(alignment_file_path)][str(ID)]['outputID'] = str(ID)
                RG_ID_dict[str(alignment_file_path)][str(ID)]['RG_tags'] = False
                if sample_description is not None:
                    RG_ID_dict[str(alignment_file_path)][str(ID)]['DS'] = str(sample_description)
                else:
                    RG_ID_dict[str(alignment_file_path)][str(ID)]['DS'] = str(
                        'LRphase_input_file_' + str(alignment_file_path)
                    )
            if str(ID) not in unique_RG_IDs:
                unique_RG_IDs[str(ID)] = {}
                unique_RG_IDs[str(ID)]['DS'] = str(sample_description)
                unique_RG_IDs[str(ID)]['SM'] = str(sample)
        elif RG_tags is not None:
            RG_ID_dict, unique_RG_IDs = _unique_RG_IDs_from_RG_tags(
                RG_ID_dict, unique_RG_IDs, alignment_file_path
            )
        else:
            print(
                str(
                    alignment_file_path
                ) + "Has No RG tags and was not input with sample information. Reads in this file will not be "
                    "processed. Either re-input this read file with sample information or resubmit with "
                    "ignore_samples option. "
            )
    return RG_ID_dict, unique_RG_IDs


def _download_file(url, output_directory=None):
    if output_directory is None:
        local_filename = url.split('/')[-1]
    else:
        local_filename = output_directory + '/' + url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            copyfileobj(r.raw, f)
    return local_filename


def _prepare_vcf_file(output_directory: str, vcf_file_input: str) -> Union[None, str]:
    """
    Checks the variant file for proper GT headers, bgzip format, and tabix indexing.
    Attempts to sort/bgzip/index if needed.
    Returns path to bgzipped/indexed vcf.

    Args:
        output_directory:
        vcf_file_input:

    Returns:
        Union[None, str]:
    """
    start_process_time = time.time()
    print('############## Preparing vcf file ##############')

    if vcf_file_input.startswith('http'):
        print('The vcf file input is a url. Downloading now.')
        vcf_file_input = _download_file(vcf_file_input, output_directory + '/haplotype_information')

    if not os.path.isfile(vcf_file_input):
        print(
            'Could not find %s. Use -v to specify the path of the vcf file to be used as haplotype information '
            'for phasing. (EX: -v path/to/GM12878.vcf.gz or --vcf GM12878.vcf).' % vcf_file_input
        )
        return

    # Check input file for proper format (GT header present, bgzipped, tabix indexed).
    # Correct the file format and index if needed.
    vcf_file_pysam: VariantFile = pysam.VariantFile(vcf_file_input)
    if vcf_file_pysam.format == 'VCF':  # What if it's not???
        # Check to be sure the GT header is present.
        if vcf_file_pysam.header.formats.keys().count('GT') == 0:
            print(
                'The VCF file provided does not have the GT subfield. VCF files must have the GT subfield for all '
                'samples in order to extract genotype information. Phased variants should have | in the GT '
                'subfield instead of / '
            )
            return

        # Check for bgzip compression.
        if vcf_file_pysam.compression == 'BGZF':
            vcf_file_path = os.path.abspath(vcf_file_input)
            print('%s is a valid vcf file' % vcf_file_path)
        # Compress with bgzip if not already done.
        else:
            print(
                '%s is a valid .vcf file but it is not in bgzip (.vcf.gz) format. VCF files must be '
                'compressed with bgzip and indexed with tabix. LRphase will now attempt to run bgzip on %s.'
                % (vcf_file_input, vcf_file_input)
            )
            # Assuming there should be a call to _sort_vcf_file here??
            vcf_file_path = _sort_vcf_file(vcf_file_input)

        # Check for a tabix index and create one if not found.
        vcf_file_index_path = vcf_file_path + '.tbi'
        if os.path.isfile(vcf_file_index_path):
            print('Found %s as an index for vcf file' % vcf_file_index_path)
        else:
            print('%s is a valid .vcf file in bgzip (.vcf.gz) format but an index was not found. Indexing with '
                  'tabix now.' % vcf_file_input)
            pysam.tabix_index(vcf_file_path, preset='vcf', force=True)
        # The VariantFile object is not stored for later use, so close it to free up resources.
        vcf_file_pysam.close()
    else:
        print("ERROR: %s is not a valid VCF file.".format(vcf_file_input))
        return

    # Calculate and report time elapsed.
    total_process_time = time.time() - start_process_time
    print(f'Prepared vcf file in {total_process_time:.2f} seconds', '\n')
    # summary_file(output_directory, time.time()-start_process_time, inspect.stack()[0][3], self.vcf_file_path)

    # Return the path to the bgzipped and indexed vcf.
    return vcf_file_path


def _parse_long_reads_input(
        long_read_input: str,
        output_directory: str
) -> Optional[Tuple[List[Optional[str]], Union[str, Any]]]:
    """

    Args:
        long_read_input (str):
        output_directory:

    Returns:
        Optional[Tuple[List[Optional[str]], Union[str, Any]]]:

    """
    if long_read_input.startswith('http'):
        print('The long read input is a url. Downloading now.')
        long_reads_alignment_path = _download_file(long_read_input, output_directory + '/input_reads')
    else:
        long_reads_alignment_path = long_read_input

    combined_long_read_fastq_path = ''  # Why is this an array? It gets assigned a string value by os.path.abspath.
    sorted_bam_file_paths = []

    if not os.path.exists(long_reads_alignment_path):
        print(
            'Could not find %s. Use -i to specify the path of a file containing reads for phasing OR use -i '
            'to specify the path of a directory containing the long read files and all files will be '
            'processed individually. (EX: -i path/minion_run3_GM12878/minion_run3_GM12878_0.fastq OR -i '
            'path/minion_run3_GM12878/minion_run3_GM12878_0.sam OR -i '
            'path/minion_run3_GM12878/minion_run3_GM12878_0_sorted.bam OR -i path/minion_run3_GM12878/).' %
            long_reads_alignment_path
        )
        return

    elif os.path.isdir(long_reads_alignment_path):
        print(
            'Directory was given as input for read files. Processing all files in %s.' % long_reads_alignment_path
        )
        for file in os.listdir(long_reads_alignment_path):
            file = '%s/%s' % (os.path.abspath(long_reads_alignment_path), file)
            if os.path.isfile(file):
                if str(file).lower().endswith('.fastq') or str(file).lower().endswith('.fastq.gz'):
                    print('%s is a valid fastq file.' % file)
                    if not combined_long_read_fastq_path:
                        combined_long_read_fastq_path = os.path.abspath(
                            '%s/%s%s' % (
                                output_directory,
                                os.path.splitext(os.path.basename(long_reads_alignment_path))[0],
                                '_combined_fastq.gz')
                        )
                    with open(combined_long_read_fastq_path, 'w') as combined_fastqs:
                        with open(file, 'r') as fastqfile:
                            combined_fastqs.write(fastqfile.read())

                elif str(file).lower().endswith('.sam') or str(file).lower().endswith('.bam'):
                    sorted_bam_file_paths.append(_prepare_alignment(output_directory, file))

    elif os.path.isfile(long_reads_alignment_path):
        if str(long_reads_alignment_path).lower().endswith('.fastq') or str(
                long_reads_alignment_path
        ).lower().endswith('.fastq.gz'):
            print('%s is a valid fastq file.' % long_reads_alignment_path)
            combined_long_read_fastq_path = os.path.abspath(
                long_reads_alignment_path
            )  # os.path.abspath('%s/%s%s' % (output_directory, os.path.splitext(
            # os.path.basename(long_reads_alignment_path))[0],'_combined_fastq.gz')) subprocess.run(['cat %s |
            # gzip >> %s' % (long_reads_alignment_path, combined_long_read_fastq_path)], check = True,
            # shell = True)

        elif str(long_reads_alignment_path).lower().endswith('.sam') or str(
                long_reads_alignment_path
        ).lower().endswith('.bam'):
            sorted_bam_file_paths.append(_prepare_alignment(output_directory, long_reads_alignment_path))
    else:
        print(
            'Error: Reads should be in .fastq, .fastq.gz, .sam, or .bam format. %s does not have a correct '
            'suffix to be a valid format and is not a directory. Use -i to specify the path of a file '
            'containing reads for phasing OR use -i to specify the path of a directory containing the long '
            'read files and all files will be processed individually. (EX: -i '
            'path/minion_run3_GM12878/minion_run3_GM12878_0.fastq OR -i '
            'path/minion_run3_GM12878/minion_run3_GM12878_0.sam OR -i '
            'path/minion_run3_GM12878/minion_run3_GM12878_0_sorted.bam OR -i path/minion_run3_GM12878/).' %
            long_reads_alignment_path
        )
        return

    return sorted_bam_file_paths, combined_long_read_fastq_path


class InputData:
    """
    sample_to_RG_header: defaultdict[Any, list]
    sample_to_PG_header: defaultdict[Any, list]
    unique_RG_IDs: Dict[Any, Any]
    """

    # output_directory: object
    # try:
    #     from LRphase import urls
    #     urls_found = True
    # except:
    #     print('Could not find import urls from data. Data will not be able to downloaded from example web sources.')
    #     urls_found = False

    def __init__(
            self, output_directory_path: str = None, vcf_file_input: str = None, long_read_input: object = None,
            reference_sequence_input: str = None, sample: str = None, ID: str = None,
            sample_description: str = None,
            ignore_phase_sets: bool = None, ignore_samples: bool = None, download_from_urls: bool = False,
            reference_sequence_input_assembly: str = None, auto_simulate_samples: bool = False,
    ) -> None:
        """

        Args:
            long_read_input (object):

        Returns:
            None:
        """
        if output_directory_path is not None:
            self.output_directory = _prepare_output_directory(output_directory_path)
        else:
            self.output_directory = _prepare_output_directory(
                'LRphase_output_' + str(time.localtime()[0]) + '-' + str(time.localtime()[1]) + '-' + str(
                    time.localtime()[2]
                ) + '_' + str(time.localtime()[3]) + 'hr_' + str(time.localtime()[4]) + 'min_' + str(
                    time.localtime()[5]
                ) + 'sec'
            )

        _prepare_output_directory(self.output_directory + '/reference_sequences')
        _prepare_output_directory(self.output_directory + '/haplotype_information')
        _prepare_output_directory(self.output_directory + '/output_reads')
        _prepare_output_directory(self.output_directory + '/input_reads')

        self.summary_file_path = _prepare_summary_file(self.output_directory)
        # self.reference_sequence_paths = None
        self.RG_ID_dict = {}
        self.unique_RG_IDs = {}
        self.vcf_files = []
        self.sample_to_vcf_file_dict = {}
        self.sample_to_reference_sequences_dict = defaultdict(list)
        self.sample_to_reference_sequence_path = defaultdict(list)
        self.sample_to_sam_header = defaultdict(list)
        self.sample_to_PG_header = defaultdict(list)
        self.sample_to_RG_header = defaultdict(list)
        self.alignment_file_to_reference_sequences_dict = defaultdict(list)
        self.alignment_files = []
        self.phasable_samples = {}
        self.reference_sequence_files = {}

        self.auto_simulate_samples = auto_simulate_samples

        # self.sample_hap_to_true_alignment_dict = {}

        self.reference_sequence_input = reference_sequence_input
        self.vcf_file_input = vcf_file_input
        self.long_read_input = long_read_input
        self.sample = sample
        self.ID = ID
        self.sample_description = sample_description
        self.ignore_phase_sets = ignore_phase_sets
        self.ignore_samples = ignore_samples
        self.download_from_urls = download_from_urls
        self.reference_sequence_input_assembly = reference_sequence_input_assembly

        if not self.reference_sequence_input_assembly is None:
            _prepare_output_directory(
                self.output_directory + '/reference_sequences/' + str(reference_sequence_input_assembly)
            )

        if not self.long_read_input is None:
            # self.long_read_input = long_read_input
            long_read_input_path, input_ID, input_sample, input_sample_description, input_reference_sequence_input = _extract_RG_info_from_long_read_input(
                long_read_input
            )
            if input_reference_sequence_input is None:
                input_reference_sequence_input = self.reference_sequence_input
            self.add_reads(
                self.long_read_input, input_sample, input_ID, input_sample_description,
                input_reference_sequence_input
            )

    # Removed commented functions. -- AGD

    def add_reference_sequence(
            self, reference_sequence_input, sample=None, output_directory=None, reference_sequence_input_assembly=None
    ) -> object:
        """
        Create an pysam.FastaFile object and store it within self.reference_sequence_files[].
        First downloads the reference sequence if supplied as a URL.
        If fasta file is bgzipped, unzips it.
        Stores absolute path to the reference sequence file in self.reference_sequence_files[].
        Returns absolute path to current reference sequence file.
        """

        # First, build the directory path where the reference sequence file will be written.
        if output_directory is None:
            output_directory_path = self.output_directory
        else:
            output_directory_path = output_directory

        if reference_sequence_input_assembly is None:
            output_directory_path = self.output_directory + '/reference_sequences'
        else:
            output_directory_path = self.output_directory + '/reference_sequences/' + str(
                reference_sequence_input_assembly)
            _prepare_output_directory(output_directory_path)

        # Download the reference sequence if a URL was provided. Reassign reference_sequence_input
        # to hold the location + name of the downloaded file.
        if reference_sequence_input.startswith('http'):
            print('The reference sequence input is a url. Downloading now.')
            reference_sequence_input = _download_file(reference_sequence_input, output_directory_path)

        # So this looks like it just reassembles the path to the given input file and applies the .fa extension.
        # Could we just test for different file types instead? reference_sequence_input_path = os.path.dirname(
        # os.path.abspath(reference_sequence_input)) + '/' + os.path.basename(reference_sequence_input).split('.')[0]
        # + '.fa'
        reference_sequence_input_path = reference_sequence_input.split('.')[0] + '.fa'  # Does same thing with less ops

        # Instantiate the pysam.FastaFile object given the supplied/downloaded file. Assign
        # this object to self.reference_sequence_files, indexed by the file path.
        try:
            ref_seq: pysam.FastaFile = pysam.FastaFile(reference_sequence_input_path)
            # reference_sequence_names = ref_seq.references
            reference_sequence_file_path: object = ref_seq.filename.decode()
            self.reference_sequence_files[reference_sequence_file_path] = ref_seq
            if reference_sequence_input_assembly:
                self.reference_sequence_files[reference_sequence_input_assembly] = ref_seq

        # If that fails, try unzipping the file with bgzip before instantiating the pysam.FastaFile
        # and making the subsequent value assignments.
        except OSError:
            # This appears to make the implicit assumption that an OSError means
            # that reference_sequence_input is a bgzip file -- maybe not always true??
            # Also, all this does is decompress the input file. Is there a way to
            # avoid this necessity? -- AGD
            with pysam.BGZFile(reference_sequence_input, 'r') as infile:
                with open(reference_sequence_input_path, 'w') as outfile:
                    outfile.write(infile.read().decode())
            ref_seq = pysam.FastaFile(reference_sequence_input_path)
            # reference_sequence_names = ref_seq.references
            reference_sequence_file_path: object = ref_seq.filename.decode()
            self.reference_sequence_files[reference_sequence_file_path] = ref_seq
            if reference_sequence_input_assembly:
                self.reference_sequence_files[reference_sequence_input_assembly] = ref_seq

        # Removed large block of commented code. --AGD

        # Store the reference sequence path to self.reference_sequence_paths[].
        # if self.reference_sequence_paths is None:
        #     self.reference_sequence_paths = reference_sequence_file_path
        # elif isinstance(self.reference_sequence_paths, str):
        #     _reference_sequence_paths = [self.reference_sequence_paths]
        #     self.reference_sequence_paths = _reference_sequence_paths
        #     self.reference_sequence_paths.append(reference_sequence_file_path)
        # elif isinstance(self.reference_sequence_paths, list):
        #     self.reference_sequence_paths.append(reference_sequence_file_path)

        if sample is None:
            if len(self.sample_to_reference_sequence_path) > 0:
                for current_sample in self.sample_to_reference_sequence_path:
                    self.sample_to_reference_sequence_path[current_sample].append(reference_sequence_file_path)
        elif isinstance(sample, str):
            self.sample_to_reference_sequence_path[sample].append(reference_sequence_file_path)

        elif isinstance(sample, list):
            for current_sample in sample:
                self.sample_to_reference_sequence_path[current_sample].append(reference_sequence_file_path)
        print(f'Reference sequence prepared successfully: {reference_sequence_file_path}')

        # Return the current reference sequence path.
        return reference_sequence_file_path  # reference_sequence_names

    def add_haplotype_information(
            self, vcf_file_input: str, ignore_phase_sets: bool = False, reference_sequence: str = 'hg38'
    ) -> object:
        """

        Args:
            vcf_file_input:
            ignore_phase_sets:
            reference_sequence:

        Returns:

        """
        # Check vcf_input_file for proper format and indexing
        vcf_file_path = _prepare_vcf_file(self.output_directory, vcf_file_input)

        # Check for phasing information
        if pysam.VariantFile(vcf_file_path).header.formats.keys().count('PS') == 0:
            ignore_phase_sets = True
            print(str(vcf_file_path) +
                  "This VCF file does not have the PS subfield. Phase sets will be ignored and all "
                  "phased variants on the same chromosome (vcf contig) will be considered to be one "
                  "contiguous haploblock "
                  )

        # Append the VCF file path to self.vcf_files[], etc.
        self.vcf_files.append({vcf_file_path: ignore_phase_sets})
        self.sample_to_vcf_file_dict = _sample_to_vcf_file_dict(self.vcf_files)
        self.sample_to_alignment_files = _sample_to_alignment_files(self.sample_to_vcf_file_dict, self.RG_ID_dict)
        self._sample_to_reference_sequences_dict()
        self._sample_to_PG_dict()

        # Return path to the vcf file.
        return vcf_file_path

    def __iter__(self):
        self.sample_counter = 0
        self.phasable_samples = {}
        return self

    def create_PhasableSample(self, sample: str, reference_sequence_names: list = None,
                              reference_sequence_paths: list = None,
                              auto_simulate_samples: bool = False,
                              output_directory: str = None, only_autosomal: bool = False,
                              regions: list = None, ploidy: int = None) -> PhasableSample.PhasableSample:
        """

        Args:
            only_autosomal:
            regions:
            ploidy:
            reference_sequence_names:
            output_directory:
            auto_simulate_samples:
            sample:
            reference_sequence_paths:

        Returns:
            PhasableSample.PhasableSample:

        """
        if output_directory is None:
            output_directory = self.output_directory + '/' + sample
        if reference_sequence_paths is None:
            auto_simulate_samples = False
        vcf_file_path, ignore_phase_sets = _pair_sample_with_vcf(
            sample, self.sample_to_vcf_file_dict, self.ignore_phase_sets
        )
        if reference_sequence_names is None:
            reference_sequence_names = self.sample_to_reference_sequences_dict[sample]
        phasable_sample = PhasableSample.PhasableSample(sample, vcf_file_path, ignore_phase_sets=ignore_phase_sets,
                                                        alignment_file_paths=self.sample_to_alignment_files[sample],
                                                        RG_ID_dict=self.RG_ID_dict,
                                                        reference_sequence_names=reference_sequence_names,
                                                        reference_sequence_paths=reference_sequence_paths,
                                                        simulate_haplotypes=auto_simulate_samples,
                                                        output_directory_path=output_directory,
                                                        only_autosomal=only_autosomal, regions=regions, ploidy=ploidy)
        return phasable_sample

    def __next__(self):
        if self.sample_counter < len(list(self.sample_to_vcf_file_dict.keys())):
            sample = str(list(self.sample_to_vcf_file_dict.keys())[self.sample_counter])
            if sample in self.sample_to_reference_sequence_path:
                if len(self.sample_to_reference_sequence_path[sample]) > 0:
                    reference_sequence_paths = self.sample_to_reference_sequence_path[sample]
                else:
                    reference_sequence_paths = None
            else:
                reference_sequence_paths = None
                # reference_sequence_paths = self.reference_sequence_paths
            phasable_sample = self.create_PhasableSample(sample, reference_sequence_paths,
                                                         auto_simulate_samples=self.auto_simulate_samples)
            # vcf_file_path, ignore_phase_sets = self._pair_sample_with_vcf(sample, self.sample_to_vcf_file_dict,
            #                                                             self.ignore_phase_sets)
            # phasable_sample = PhasableSample(sample, vcf_file_path, ignore_phase_sets,
            #                               self.sample_to_alignment_files[sample], self.RG_ID_dict)
            self.sample_counter += 1
            self.phasable_samples[phasable_sample.sample] = phasable_sample
            return phasable_sample
        else:
            raise StopIteration()

    def add_reads(
            self, long_reads_alignment_path: str, sample: str = None, ID: object = None, haplotype: object = None,
            sample_description: str = None,
            reference_sequence_input: str = None, database: object = None, master_database: bool = False,
            simulated: bool = False,
            reference_sequence_input_assembly: str = None
    ) -> object:
        """
        Args:
            long_reads_alignment_path:
            sample:
            ID:
            haplotype:
            sample_description:
            reference_sequence_input:
            database:
            master_database:
            simulated:
            reference_sequence_input_assembly:

        Returns:
            object:
        """
        # if reference_sequence_input == None:
        # reference_sequence_input = self.reference_sequence_input
        if long_reads_alignment_path.startswith('http'):
            print('The reads input is a url. Downloading now.')
            long_reads_alignment_path = _download_file(long_reads_alignment_path, self.output_directory)

        sorted_bam_file_paths, combined_long_read_fastq_path = _parse_long_reads_input(
            long_reads_alignment_path, self.output_directory
        )
        if combined_long_read_fastq_path:
            reference_sequence_input = self.add_reference_sequence(
                reference_sequence_input=reference_sequence_input, output_directory=self.output_directory,
                reference_sequence_input_assembly=reference_sequence_input_assembly
            )
            if reference_sequence_input is None:
                if self.reference_sequence_input is None:
                    print('Need reference sequence')
                    return
                else:
                    reference_sequence_input = self.reference_sequence_input
            sorted_bam_file_paths.append(
                _align_long_reads_fastq(
                    combined_long_read_fastq_path, reference_sequence_input, self.output_directory
                )
            )
        for _sorted_bam_file_path in sorted_bam_file_paths:
            if _sorted_bam_file_path:
                sorted_bam_file_path, combined_long_read_fastq_path = _parse_long_reads_input(
                    _sorted_bam_file_path, self.output_directory
                )
                self.RG_ID_dict, self.unique_RG_IDs = _compile_read_groups(
                    sorted_bam_file_path[0], sample, ID, sample_description, self.RG_ID_dict, self.unique_RG_IDs,
                    self.ignore_samples
                )
                self.alignment_files.append(sorted_bam_file_path[0])
                self.sample_to_alignment_files = _sample_to_alignment_files(
                    self.sample_to_vcf_file_dict, self.RG_ID_dict
                )
                self._sample_to_reference_sequences_dict(sorted_bam_file_path[0])
                self._sample_to_PG_dict(sam_file_path=sorted_bam_file_path[0])
                if reference_sequence_input is not None:
                    if not reference_sequence_input in self.sample_to_reference_sequence_path[sample]:
                        self.sample_to_reference_sequence_path[sample].append(reference_sequence_input)

    def _prepare_sam_header(self, _sample: str = None) -> None:
        """

        Args:
            _sample (object):

        Returns:
            None:
        """
        if not str(_sample) in self.sample_to_sam_header:
            self.sample_to_sam_header[_sample] = defaultdict(list)
        self.sample_to_sam_header[_sample]['HD'] = {'VN': '1.6', 'SO': 'coordinate'}
        self.sample_to_sam_header[_sample]['SQ'] = self.sample_to_reference_sequences_dict[_sample]
        self.sample_to_sam_header[_sample]['RG'] = self.sample_to_RG_header[_sample]
        self.sample_to_sam_header[_sample]['PG'] = self.sample_to_PG_header[_sample]
        # return  # self.sample_to_sam_header[_sample]

    def _sample_to_reference_sequences_dict(self, sam_file_path: str = None, sam_file: object = None) -> None:
        """
        Prepare a dictionary relating reference sequences to samples.

        Args:
            sam_file_path:
            sam_file:

        Returns:
            None:
        """
        if sam_file_path:
            aln_file = pysam.AlignmentFile(sam_file_path)
            for reference_sequence in aln_file.header['SQ']:
                self.alignment_file_to_reference_sequences_dict[sam_file_path].append(reference_sequence)
            aln_file.close()
        for sample in self.sample_to_vcf_file_dict:
            for sam_file_path in self.alignment_file_to_reference_sequences_dict:
                if sam_file_path in self.sample_to_alignment_files[str(sample)]:
                    aln_file = pysam.AlignmentFile(sam_file_path)
                    for reference_sequence in aln_file.header['SQ']:
                        if str(reference_sequence['SN']) not in [str(reference_seq['SN']) for reference_seq in
                                                                 self.sample_to_reference_sequences_dict[sample]]:
                            self.sample_to_reference_sequences_dict[sample].append(reference_sequence)
                    aln_file.close()

    def _sample_to_PG_dict(self, sam_file_path: str = None, sam_file: object = None) -> None:
        """
        Creates a dictionary relating samples to phasing groups.
        Args:
            sam_file_path:
            sam_file:

        Returns:
            None:
        """
        if sam_file_path:
            aln_file = pysam.AlignmentFile(sam_file_path)
            for reference_sequence in aln_file.header['SQ']:
                self.alignment_file_to_reference_sequences_dict[sam_file_path].append(reference_sequence)
            aln_file.close()
        for sample in self.sample_to_vcf_file_dict:
            for sam_file_path in self.alignment_file_to_reference_sequences_dict:
                if sam_file_path in self.sample_to_alignment_files[str(sample)]:
                    aln_file = pysam.AlignmentFile(sam_file_path)
                    for PG_tag in aln_file.header['PG']:
                        PG_tag['ID'] = str(list(self.RG_ID_dict[sam_file_path].keys())[0])
                        # if PG_tag['ID'] in [PG_tag['ID'] for PG_tag in self.sample_to_PG_header[sample]]
                        RG_tag = {
                            'ID': str(list(self.RG_ID_dict[sam_file_path].keys())[0]), 'SM': str(
                                self.RG_ID_dict[sam_file_path][
                                    str(list(self.RG_ID_dict[sam_file_path].keys())[0])]['SM']
                            ),
                            'DS': str(
                                self.RG_ID_dict[sam_file_path][
                                    str(list(self.RG_ID_dict[sam_file_path].keys())[0])]['DS']
                            )
                        }
                        # {str(list(self.RG_ID_dict[sam_file_path].keys())[0]): {'DS': 'small7.fastq', 'SM': 'HG001',
                        # 'RG_tags': True, 'outputID': '1'}} self.RG_ID_dict[sam_file_path] self.RG_ID_dict[
                        # sam_file_path][str(list(self.RG_ID_dict[sam_file_path].keys())[0])]['SM'] if not PG_tag[
                        # 'ID'] in [PG_tag['ID'] for PG_tag in self.sample_to_PG_header[sample]]:
                        # self.sample_to_PG_header[sample].append(PG_tag)
                        new_PG_tag: bool = True
                        for PG_header in self.sample_to_PG_header[sample]:
                            if PG_tag['PN'] == PG_header['PN'] and PG_tag['ID'] == PG_header['ID']:
                                new_PG_tag = False
                        if new_PG_tag:
                            self.sample_to_PG_header[sample].append(PG_tag)
                        # self.sample_to_PG_header[sample].append(PG_tag)
                        if not RG_tag['ID'] in [RG_tag['ID'] for RG_tag in self.sample_to_RG_header[sample]]:
                            self.sample_to_RG_header[sample].append(RG_tag)
                    aln_file.close()
