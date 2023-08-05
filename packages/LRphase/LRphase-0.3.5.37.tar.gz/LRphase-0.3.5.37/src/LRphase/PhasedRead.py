import math
import os
from collections import defaultdict
from typing import Union, Any, Optional

import pysam
from pysam import VariantFile

# import numpy as np
import pyliftover
from LRphase import PhasableSample
from LRphase import PhaseSet

class LongRead:

    """

    """

    def __init__(self, read_name, read_sequence, read_sequence_qualities):
        self.name = read_name
        self.sequence = read_sequence
        self.qualities = read_sequence_qualities


def true_alignment_match(
        aligned_segment: pysam.AlignedSegment,
        needs_liftover: object = False,
        contig: object = None,
        ref_start: object = None,
        ref_end: object = None,
        strand: object = None,
        tag_read: object = False,
        only_output_match_label: object = False,
        only_output_overlap: object = False,
        true_reference_sequence_path: object = None,
        aligned_reference_sequence_path: object = None,
        liftover_converter: object = None,
        chain_file_path: object = None,
        sample: object = None,
        haplotype: object = None,
        reference_liftover_converters: object = None
) -> object:
    """
    Args:
        haplotype:
        reference_liftover_converters:
        aligned_segment (object):
        needs_liftover:
        contig:
        ref_start (object):
        ref_end:
        strand:
        tag_read:
        only_output_match_label:
        only_output_overlap:
        true_reference_sequence_path:
        aligned_reference_sequence_path (object):
        liftover_converter:
        chain_file_path (object):
        sample:

    Returns:
    
    """
    overlap = 0
    match_label = 'non_match'

    if contig is None or ref_start is None or ref_end is None or strand is None:
        contig, ref_start, ref_end, strand = true_alignment_coordinates(
            aligned_segment, tag_read=tag_read, contig=contig, ref_start=ref_start, ref_end=ref_end,
            strand=strand
        )

    if needs_liftover:
        if liftover_converter is not None:
            liftover_converter = liftover_converter

        elif reference_liftover_converters is not None:
            if aligned_reference_sequence_path is not None:
                if aligned_reference_sequence_path in reference_liftover_converters:
                    if sample in reference_liftover_converters[aligned_reference_sequence_path]:
                        if str(haplotype) in reference_liftover_converters[aligned_reference_sequence_path][sample]:
                            liftover_converter = reference_liftover_converters[aligned_reference_sequence_path][sample][
                                str(haplotype)]

        elif chain_file_path is not None:
            if os.path.isfile(chain_file_path):
                liftover_converter = pyliftover.Liftover(chain_file_path)

        else:
            print('could not liftover')
            return

        contig = liftover_converter.convert_coordinate(contig, ref_start)[0][0]
        ref_start = liftover_converter.convert_coordinate(contig, ref_start)[0][1]
        ref_end = liftover_converter.convert_coordinate(contig, ref_end)[0][1]
        strand = liftover_converter.convert_coordinate(contig, ref_start)[0][2]

    if aligned_segment.reference_name == contig:
        match_label = 'ref_match'
        if int(ref_start) <= int(aligned_segment.reference_start) <= int(
                ref_end
        ):
            match_label = 'mapping_match'
            if int(aligned_segment.reference_end) >= int(ref_end):
                overlap = int(ref_end) - int(aligned_segment.reference_start)
            else:
                overlap = int(aligned_segment.reference_end) - int(aligned_segment.reference_start)
        elif int(ref_start) <= int(aligned_segment.reference_end) <= int(
                ref_end
        ):
            match_label = 'mapping_match'
            if int(ref_start) >= int(aligned_segment.reference_start):
                overlap = int(aligned_segment.reference_end) - int(ref_start)
            else:
                overlap = int(aligned_segment.reference_end) - int(aligned_segment.reference_start)
        elif (
                int(ref_start) - (int(ref_start) * 0.1)) <= aligned_segment.reference_start <= (
                int(ref_end) + (int(ref_end) * 0.1)):
            match_label = 'within_10percent'

    if tag_read:
        aligned_segment.set_tag(
            tag='ov', value=str(overlap / (int(ref_end) - int(ref_start))), value_type='Z', replace=True
        )
        aligned_segment.set_tag(
            tag='OV', value=str(overlap / aligned_segment.query_alignment_length), value_type='Z',
            replace=True
        )
        aligned_segment.set_tag(tag='ml', value=str(match_label), value_type='Z', replace=True)

    if only_output_match_label:
        return match_label

    elif only_output_overlap:
        return overlap

    else:
        return match_label, overlap


def true_alignment_coordinates(
        aligned_segment: pysam.AlignedSegment, tag_read: bool = False, contig: str = None, ref_start: int = None,
        ref_end: int = None, strand: str = None
) -> object:
    """

    Args:
        aligned_segment:
        tag_read:
        contig:
        ref_start:
        ref_end:
        strand:

    Returns:

    """
    if '!' in str(aligned_segment.query_name):
        _read_name, _contig, _ref_start, _ref_end, _strand = aligned_segment.query_name.split('!')
        if contig is None:
            contig = _contig
        if ref_start is None:
            ref_start = _ref_start
        if ref_end is None:
            ref_end = _ref_end
        if strand is None:
            strand = _strand

    if tag_read:
        aligned_segment.set_tag(tag='st', value=str(ref_start), value_type='Z', replace=True)
        aligned_segment.set_tag(tag='lo', value=str(contig), value_type='Z', replace=True)
        aligned_segment.set_tag(tag='en', value=str(ref_end), value_type='Z', replace=True)
        aligned_segment.set_tag(tag='sd', value=str(strand), value_type='Z', replace=True)

    return contig, ref_start, ref_end, strand


def true_read_origin(
        aligned_segment: pysam.AlignedSegment, tag_read: bool = False, sample: str = None, haplotype: object = None,
        contig: str = None,
        ref_start: int = None,
        ref_end: int = None, strand: str = None
) -> object:
    """

    Args:
        aligned_segment:
        tag_read:
        sample:
        haplotype:
        contig:
        ref_start:
        ref_end:
        strand:

    Returns:

    """
    if '!' in str(aligned_segment.query_name):
        _ref_start: object
        _read_name, _contig, _ref_start, _ref_end, _strand = aligned_segment.query_name.split('!')
        if contig is None:
            contig = _contig
        if ref_start is None:
            ref_start = _ref_start
        if ref_end is None:
            ref_end = _ref_end
        if strand is None:
            strand = _strand

        if '__' in _read_name:
            sample, haplotype, name_contig_numeric = _read_name.split('__')

    if tag_read:
        aligned_segment.set_tag(tag='sm', value=str(sample), value_type='Z', replace=True)
        aligned_segment.set_tag(tag='ha', value=str(haplotype), value_type='Z', replace=True)

    return sample, haplotype


def alignment_type(aligned_segment: pysam.AlignedSegment, tag_read: bool = False) -> object:
    """

    Args:
        aligned_segment:
        tag_read:

    Returns:

    """
    alignmenttype = 'None'
    if aligned_segment.is_unmapped:
        alignmenttype = 'unmapped'
    elif aligned_segment.is_secondary:
        alignmenttype = 'secondary'
    elif aligned_segment.is_supplementary:
        alignmenttype = 'supplementary'
    else:
        alignmenttype = 'mapped'
    if tag_read:
        aligned_segment.set_tag(tag='al', value=str(alignmenttype), value_type='Z', replace=True)

    return alignmenttype


def _fetch_phased_variants(aligned_segment: pysam.AlignedSegment, vcf_file: Union[VariantFile, str], sample: str,
                           ignore_phase_sets: bool = False) -> defaultdict(list):
    """

    Args:
        aligned_segment:
        vcf_file:
        sample:
        ignore_phase_sets:

    Returns:
        defaultdict(list):

    """

    variants_phase_sets = defaultdict(list)

    if isinstance(vcf_file, VariantFile):
        vcf_in = vcf_file
    elif isinstance(vcf_file, str):
        vcf_in = VariantFile(vcf_file)
    else:
        return variants_phase_sets

    for vcf_record in vcf_in.fetch(
            aligned_segment.reference_name, aligned_segment.reference_start, aligned_segment.reference_end
    ):
        if vcf_record.samples[str(sample)].phased and max(vcf_record.samples[str(sample)].allele_indices) > min(
                vcf_record.samples[str(sample)].allele_indices
        ):
            if ignore_phase_sets:
                variants_phase_sets['ignore_phase_sets'].append(vcf_record)
            else:
                variants_phase_sets[str(vcf_record.samples[str(sample)]['PS'])].append(vcf_record)
    vcf_in.close()

    return variants_phase_sets


def powlaw_modified(x: float, a: float = 4.5, xmin: float = 2) -> float:
    """

    Args:
        x:
        a:
        xmin:

    Returns:

    """
    return ((a - 1) / xmin) * math.pow(x / xmin, -1 * a)

class PhasedRead:
    """

    """

    def __init__(
            self, aligned_segment: pysam.AlignedSegment, phasable_sample: PhasableSample.PhasableSample = None,
            vcf_file: str = None, sample: str = None, haplotype: object = None,
            ignore_phase_sets: bool = False, error_model: int = 0,
            error_rate_threshold: float = 0.01,
            prior_probabilities: object = None, bam_file_header: object = None, output_file_path: str = None,
            liftover_converters: object = None,
            multinomial_correction: bool = True, auto_phase: bool = True, evaluate_alignment: bool = True,
            evaluate_true_alignment: bool = False, aligned_reference_sequence_path: str = None
    ) -> object:
        self.output_file_path = None
        self.liftover_converters = None
        self.aligned_segment = aligned_segment
        self.aligned_reference_sequence_path = None
        self.needs_liftover = False
        self.true_reference_sequence_path = None

        if isinstance(phasable_sample, PhasableSample.PhasableSample):
            self.vcf_file = phasable_sample.vcf_file_path
            self.sample = phasable_sample.sample
            if phasable_sample.simulate_haplotypes:
                if output_file_path is None:
                    self.output_file_path = phasable_sample.output_directory
                self.liftover_converters = phasable_sample.haplotype_liftover_converters
                self.aligned_reference_sequence_path = phasable_sample.reference_sequence_path
                self.needs_liftover = True
                self.evaluate_true_alignment = True

        else:
            self.vcf_file = vcf_file
            self.sample = sample

        self.haplotype = haplotype
        self.ignore_phase_sets = ignore_phase_sets
        self.error_model = error_model
        self.multinomial_correction = multinomial_correction
        self.error_rate_threshold = error_rate_threshold
        self.prior_probabilities = prior_probabilities
        # self._get_alignment_label()
        if self.liftover_converters is None:
            self.liftover_converters = liftover_converters
        self.auto_phase = auto_phase
        self._Phase_Set_max = None
        self.PhaseSets = []
        self.evaluate_alignment = evaluate_alignment
        self.evaluate_true_alignment = evaluate_true_alignment

        if output_file_path:
            self.output_file_path = output_file_path
        elif self.output_file_path is None:
            self.output_file_path = '%s_phase_tagged.bam' % self.sample

        if bam_file_header:
            self.bam_file_header = bam_file_header
        if self.evaluate_alignment:
            alignment_type(self.aligned_segment, tag_read=True)
            # self._evaluate_alignment()
        if self.evaluate_true_alignment:
            true_alignment_match(
                self.aligned_segment,
                needs_liftover=self.needs_liftover,
                contig=None,
                ref_start=None,
                ref_end=None,
                strand=None,
                tag_read=True,
                only_output_match_label=False,
                only_output_overlap=False,
                true_reference_sequence_path=self.true_reference_sequence_path,
                aligned_reference_sequence_path=self.aligned_reference_sequence_path,
                liftover_converter=self.liftover_converters,
                chain_file_path=None,
                sample=self.sample,
                haplotype=self.haplotype,
                reference_liftover_converters=None
            )

        if self.auto_phase:
            self.phase_read(
                error_model=self.error_model, error_rate_threshold=self.error_rate_threshold,
                multinomial_correction=self.multinomial_correction,
            )

    def __repr__(self):
        return f'Read Name: {self.query_name}, Is phased: {self.is_Phased}, Favors single phase: {self.one_phase_is_favored}\nRead Length: {self.aligned_segment.query_length}\nAlignment Type: {self.alignment_type}\nPrimary Alignment Length: {self.aligned_segment.query_alignment_length} '

    def __iter__(self):
        self.PhaseSets = self._find_PhaseSets(
            self.error_model, self.error_rate_threshold, self.prior_probabilities,
            liftover_converters=self.liftover_converters
        )
        self.PhaseSets_processed_count = 0
        # self.alignment_files_read_counts = [bam_file.mapped+bam_file.unmapped for bam_file in self.bam_files]
        return self

    def __next__(self):
        if self.PhaseSets_processed_count < len(self.PhaseSets):
            Phase_Set = self.PhaseSets[self.PhaseSets_processed_count]
            self.PhaseSets_processed_count += 1
            return Phase_Set
        else:
            raise StopIteration()

    def _find_PhaseSets(self, error_model, error_rate_threshold, prior_probabilities, liftover_converters=None):

        if liftover_converters is None:
            liftover_converters = self.liftover_converters

        al_type = alignment_type(self.aligned_segment, tag_read=True)

        if self.aligned_segment.is_unmapped:
            self._Phase_Set_max = 'unmapped'
            return 'Nonphasable'

        if self.aligned_segment.get_tag('al') == 'aligned_to_contig_not_in_vcf' or self.aligned_segment.is_unmapped:
            return 'aligned_to_contig_not_in_vcf'

        variants_phase_sets = _fetch_phased_variants(
            self.aligned_segment, self.vcf_file, self.sample, self.ignore_phase_sets
        )

        PhaseSets = []
        if len(variants_phase_sets) > 0:
            if max([len(variants_phase_sets[str(phase_set)]) for phase_set in variants_phase_sets]) > 0:
                for phase_set in variants_phase_sets:
                    PhaseSets.append(
                        PhaseSet.PhaseSet(
                            phase_set,
                            self.aligned_segment,
                            variants_phase_sets[str(phase_set)],
                            str(self.sample),
                            error_model=error_model,
                            error_rate_threshold=error_rate_threshold,
                            prior_probabilities=prior_probabilities,
                            liftover_converters=liftover_converters
                        )
                    )

        return PhaseSets

    def phase_read(
            self,
            error_model: int = None,
            error_rate_threshold: float = None,
            prior_probabilities: object = None,
            multinomial_correction: bool = None
    ) -> object:
        """

        Args:
            error_model:
            error_rate_threshold:
            prior_probabilities:
            multinomial_correction:

        Returns:

        """
        if error_model is None:
            error_model = self.error_model
        if error_rate_threshold is None:
            error_rate_threshold = self.error_rate_threshold
        if multinomial_correction is None:
            multinomial_correction = True

        # if evaluate_alignment:
        # self._evaluate_alignment()
        # if evaluate_true_alignment:
        #    if self.aligned_segment.has_tag('oa'):
        #        match_label = self._evaluate_true_alignment

        if not self.aligned_segment.has_tag('al'):
            alignment_type(self.aligned_segment, tag_read=True)

        # if not self.aligned_segment.has_tag('ml'):
        #    if self.aligned_segment.has_tag('oa'):
        #        match_label = self._evaluate_true_alignment

        _Phase_Set_max = self._select_best_phasing(
            self._find_PhaseSets(error_model, error_rate_threshold, prior_probabilities,
                                 liftover_converters=self.liftover_converters),
            error_model,
            error_rate_threshold,
            prior_probabilities,
            multinomial_correction
        )

        self._Phase_Set_max = _Phase_Set_max
        # self.aligned_segment.set_tag(tag = 'PS', value = str(self.phase_set_name), value_type='Z', replace=True)
        # self.aligned_segment.set_tag(tag = 'HP', value = str(self.phase), value_type='Z', replace=True)
        # self.aligned_segment.set_tag(tag = 'PC', value = str(self.log_likelihood_ratio), value_type='Z', replace=True)
        # self.aligned_segment.set_tag(tag = 'py', value = str(self.ploidy_phase_set), value_type='Z', replace=True)

        return self

    def _select_best_phasing(
            self, PhaseSets: list, error_model: int = 0, error_rate_threshold: float = 0.01,
            prior_probabilities: object = None,
            multinomial_correction: bool = True
    ) -> Union[str, PhaseSet.PhaseSet]:
        """

        Args:
            PhaseSets (object):
            error_model:
            error_rate_threshold:
            prior_probabilities:
            multinomial_correction:

        Returns:

        """
        self.PhaseSets = PhaseSets
        phasable = {}
        if isinstance(PhaseSets, str):
            return 'Nonphasable'

        if len(PhaseSets) > 0:
            for Phase_Set in PhaseSets:
                Phase_Set.solve_phase(error_model, error_rate_threshold, prior_probabilities, multinomial_correction)
                if isinstance(Phase_Set.max_log_likelihood_ratio, float):
                    phasable[Phase_Set.max_log_likelihood_ratio] = Phase_Set

        if len(phasable) > 0:
            Phase_Set_max = phasable[max(phasable.keys())]
            # phase = Phase_Set_max.phase
            # phase_set_name = Phase_Set_max.phase_set
            # log_likelihood_ratio = Phase_Set_max.max_log_likelihood_ratio
            # max_phase = Phase_Set_max.max_phase
            Phase_Set_max = Phase_Set_max

        else:
            # phase = 'Nonphasable'
            # phase_set_name = None
            # log_likelihood_ratio = None
            # max_phase = 'Nonphasable'
            Phase_Set_max = 'Nonphasable'

        return Phase_Set_max  # phase, phase_set_name, log_likelihood_ratio, max_phase

    # @staticmethod

    @property
    def read_name(self) -> str:
        """

        Returns:
            str:

        """
        return str(self.aligned_segment.query_name)

    @property
    def query_name(self) -> str:
        """

        Returns:
            str:

        """
        return str(self.aligned_segment.query_name)

    @property
    def alignment_type(self) -> str:
        """

        Returns:
            str:

        """
        if self.aligned_segment.has_tag('al'):
            return str(self.aligned_segment.get_tag('al'))

    @property
    def alignment_is_unmapped(self) -> bool:
        """

        Returns:
            bool:

        """
        return self.aligned_segment.is_unmapped

    @property
    def alignment_is_supplementary(self) -> bool:
        """

        Returns:
            bool:

        """
        return self.aligned_segment.is_supplementary

    @property
    def alignment_is_secondary(self) -> bool:
        """

        Returns:
            bool:

        """
        return self.aligned_segment.is_secondary

    @property
    def is_aligned_to_contig_not_in_vcf(self) -> bool:
        """

        Returns:
            bool:

        """
        return self.aligned_segment.reference_name not in list(self.vcf_file.index)

    @property
    def alignment_is_reverse(self) -> bool:
        """
        true if aligned_segment is mapped to reverse strand

        Returns:
            bool:
        """
        return self.aligned_segment.is_reverse

    @property
    def alignment_is_mapped(self) -> bool:
        """

        Returns:
            bool:

        """
        return self.aligned_segment.is_unmapped == False

    @property
    def alignment_is_primary(self) -> bool:
        """

        Returns:
            bool:

        """
        if self.aligned_segment.has_tag('tp'):
            return str(self.aligned_segment.get_tag('tp')) == 'P'
        # return self.aligned_segment.is_unmapped == False

    @property
    def alignment_length_fraction_of_total_read_length(self) -> float:

        """
        aligned_segment.query_alignment_length/aligned_segment.query_length
        returns 0 if unmapped

        Returns:
            float:
        """
        # self.aligned_segment.set_tag(tag = 'xx', value = str(
        # self.aligned_segment.query_alignment_length/self.aligned_segment.query_length), value_type='Z', replace=True)
        if self.aligned_segment.has_tag('al'):
            if str(self.aligned_segment.get_tag('al')) == 'unmapped_reads':
                return 0.0
            return self.aligned_segment.query_alignment_length / self.aligned_segment.query_length

    @property
    def is_Nonphasable(self) -> Union[None, str, bool]:
        """
        Returns True if this aligned_segment was assigned Nonphasable for not having any heterozygous positions

        Returns:
            Union[None, str, bool]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return True
        else:
            return self.phase == 'Nonphasable'

    @property
    def is_Unphased(self) -> Union[None, str, bool]:
        """
        Returns True if this aligned_segment was left unassigned (Unphased) because it did not have a log likelihood ratio (LR)
        above the threshold chosen for this experiment.

        Returns:
            Union[None, str, bool]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        else:
            return self.phase == 'Unphased'

    @property
    def is_Phased(self) -> Union[None, str, bool]:
        """
        Returns True if this aligned_segment was assigned to a haplotype based on its log likelihood ratio (LR) being above the
        threshold chosen for this experiment.

        Returns:
            Union[None, str, bool]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        else:
            if self.phase == 'Unphased' or self.phase == 'Nonphasable':
                is_Phased = False
            else:
                is_Phased = True
            return is_Phased

    @property
    def one_phase_is_favored(self) -> Union[None, str, bool]:
        """
        Returns True if this aligned_segment was assigned to a haplotype based on its log likelihood ratio (LR) being above the
        threshold chosen for this experiment.

        Returns:
            Union[None, str, bool]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        else:
            if int(self.max_phase) > 0:
                one_phase_is_favored = True
            elif int(self.max_phase) == 0:
                one_phase_is_favored = False
            else:
                return
            return one_phase_is_favored

    def is_assigned_to_haplotype_i(self, haplotype: int) -> Union[None, str, bool]:

        """
        Returns True if this aligned_segment was was assigned to haplotype i. (ie: the index of the haplotype in the allele_indices A|T )

        Args:
            haplotype:

        Returns:
            Union[None, str, bool]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        else:
            return str(self.phase) == str(haplotype)

    @property
    def overlaps_multiple_phase_sets(self) -> Union[None, str, bool]:
        """
        This aligned_segment overlapped heterozygous positions that belonged to at least two different phase sets (independently
        phased blocks of sequence are only phased within themselves and one must be chosen)

        Returns:
            Union[None, str, bool]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        if len(self.PhaseSets) > 1:
            overlaps_multiple_phase_sets = True
        else:
            overlaps_multiple_phase_sets = False
        return overlaps_multiple_phase_sets

    @property
    def Phase_Set_max(self) -> Union[None, str, PhaseSet.PhaseSet]:

        """

        Returns:
            Union[None, str, PhaseSet.PhaseSet]:

        """
        if self._Phase_Set_max is None:
            return
        elif self._Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self._Phase_Set_max

    @property
    def phase(self) -> Union[None, str, int]:
        """

        Returns:
            Union[None, str, int]:

        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.phase

    @property
    def max_phase(self) -> Union[None, str, int]:
        """
        The number of distinct haplotypes at this position. Our model assumes that ploidy represents the ground truth
        molecular copy number of the population from which these reads were samples.

        Returns:
            Union[None, str, int]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.max_phase

    @property
    def phase_set_name(self) -> Optional[str]:
        """
        The number of distinct haplotypes at this position. Our model assumes that ploidy represents the ground truth
        molecular copy number of the population from which these reads were samples.

        Returns:
            object:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.phase_set

    @property
    def phasing_error_rate(self) -> float:
        """

        Returns:
            float:

        """
        if self.phase == 'Nonphasable':
            return 0.50
        if self.log_likelihood_ratio > 0:
            if powlaw_modified(self.log_likelihood_ratio) <= 1 - (1 / float(self.ploidy_phase_set)):
                return powlaw_modified(self.log_likelihood_ratio)
            else:
                return 1 - (1 / float(self.ploidy_phase_set))

    @property
    def log_likelihood_ratio(self) -> Union[None, str, float]:
        """
        The number of distinct haplotypes at this position. Our model assumes that ploidy represents the ground truth
        molecular copy number of the population from which these reads were samples.

        Returns:
            Union[None, str, float]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.max_log_likelihood_ratio

    @property
    def ploidy_phase_set(self) -> Union[Optional[str], int]:
        """
        The number of distinct haplotypes at this position. Our model assumes that ploidy represents the ground truth
        molecular copy number of the population from which these reads were samples.

        Returns:
            Union[Optional[str], int]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.ploidy_phase_set

    @property
    def error_model_used(self) -> Union[None, str, int]:
        """
        self.aligned_segment.set_tag(tag = 'em', value = str(self.error_model), value_type='Z', replace=True)

        Returns:
            Union[None, str, int]:

        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.error_model_used

    @property
    def multinomial_correction_used(self) -> Union[None, str, bool]:
        """
        self.aligned_segment.set_tag(tag = 'em', value = str(self.error_model), value_type='Z', replace=True)

        Returns:
            Union[None, str, bool]:

        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        else:
            return self.Phase_Set_max.multinomial_correction

    @property
    def error_rate_threshold_used(self) -> Union[None, str, float]:
        """

        self.aligned_segment.set_tag(tag = 'et', value = str(self.error_rate_threshold), value_type='Z', replace=True)

        Returns:
            Union[None, str, float]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.error_rate_threshold_used

    @property
    def prior_probabilities_used(self) -> Union[None, str, list]:
        """

        self.aligned_segment.set_tag(tag = 'et', value = str(self.error_rate_threshold), value_type='Z', replace=True)

        Returns:
            Union[None, str, list]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.prior_probabilities_used

    @property
    def error_rate_average_het_sites_used(self) -> Union[None, str, float]:
        """

        self.aligned_segment.set_tag(tag = 'er', value = str(Phase_Set_max.error_rate_average_het_sites_used), value_type='Z', replace=True)

        Returns:
            Union[None, str, float]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.error_rate_average_het_sites

    @property
    def per_base_mismatch_rate_used(self) -> Union[None, str, float]:
        """

        self.aligned_segment.set_tag(tag = 'er', value = str(Phase_Set_max.error_rate_average_het_sites_used), value_type='Z', replace=True)

        Returns:
            Union[None, str, float]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.per_base_mismatch_rate

    @property
    def total_hets_analyzed_favored_haplotype(self) -> Union[None, str, int]:
        """
        Returns the total number of heterozygous positions that were included in the phasing evaluation for this aligned_segment
        that resulted in the most favorable likelihood (ie: positions containing heterozygous SNVs that align to the
        aligned_segment of interest.)

        Returns:
            Union[None, str, int]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.total_hets_analyzed

    @property
    def total_hets_favored_haplotype(self) -> Union[None, str, int]:
        """
        Returns the total number of heterozygous positions that overlapped this aligned_segment before filtering the sites with
        '-'. This set of het sites was the most favorable phase set that resulted in the most favorable likelihood (
        ie: positions containing heterozygous SNVs that align to the aligned_segment of interest.)

        Returns:
            Union[None, str, int]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.total_hets

    @property
    def total_matches_to_favored_haplotype(self) -> Union[None, str, int]:
        """
        Returns the total number of matches to the favored haplotype sequence at heterozygous positions that
        overlapped this aligned_segment. This phased set of het sites resulted in the most favorable likelihood for this aligned_segment.

        Returns:
            Union[None, str, int]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.matches[self.Phase_Set_max.max_phase - 1]

    @property
    def total_non_matches_to_favored_haplotype(self) -> Union[None, str, int]:
        """
        Returns the total number of non-matches to the favored haplotype sequence at heterozygous positions that
        overlapped this aligned_segment. This phased set of het sites resulted in the most favorable likelihood for this aligned_segment.

        Returns:
            Union[None, str, int]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.non_matches[self.Phase_Set_max.max_phase - 1]

    def prior_probability_for_haplotype_i(self, i: int) -> Union[None, str, float]:
        """
        self.aligned_segment.set_tag(tag = 'pr', value = str(self.prior_probabilities), value_type='Z', replace=True)


        prior_probability_haplotype_i = P(haplotype_i)

        Args:
            i:

        Returns:
            Union[None, str, float]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.prior_probabilities[i - 1]

    @property
    def prior_probability_for_favored_haplotype(self) -> Union[None, str, float]:
        """
        self.aligned_segment.set_tag(tag = 'pr', value = str(self.prior_probabilities), value_type='Z', replace=True)

        prior_probability_haplotype_i = P(haplotype_i)

        Returns:
            Union[None, str, float]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.prior_probabilities[self.max_phase - 1]

    def calculate_log_likelihood_read_given_haplotype_i(self, i: int) -> Union[None, str, float]:
        """

        Args:
            i:

        Returns:
            Union[None, str, float]:

        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.log_probability_read_given_haplotype_i[i - 1]

    def calculate_likelihood_of_read_given_haplotype_i(self, i: int) -> Union[None, str, float]:
        """

        Args:
            i:

        Returns:
            Union[None, str, float]:

        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return 10 ** self.Phase_Set_max.log_probability_read_given_haplotype_i[i - 1]

    @property
    def calculate_log_likelihood_read_given_favored_haplotype(self) -> Union[None, str, float]:
        """

        Returns:
            Union[None, str, float]:

        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.Phase_Set_max.log_probability_read_given_haplotype_i[self.max_phase - 1]

    @property
    def calculate_likelihood_of_read_given_favored_haplotype(self) -> Union[None, str, float]:
        """

        Returns:
            Union[None, str, float]:

        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return 10 ** self.Phase_Set_max.log_probability_read_given_haplotype_i[self.max_phase - 1]

    @property
    def bayes_numerator_for_favored_haplotype(self) -> Union[None, str, float]:
        """
        P(aligned_segment|haplotype_i)P(haplotype_i)
        Bayes numerator. likelihood * prior

        Returns:
            Union[None, str, float]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.calculate_likelihood_of_read_given_haplotype_i(
                self.max_phase - 1
            ) * self.prior_probability_for_haplotype_i(self.max_phase - 1)
        # if self.likelihood_for_haplotype_i(i) and self.prior_probability_for_haplotype_i(i):

    @property
    def log_likelihood_ratio_for_favored_haplotype_vs_not_favored_haplotype(self) -> Union[None, str, float]:
        """

        Returns:
            Union[None, str, float]:

        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            if self.total_probability_of_read_given_haplotypes and self.bayes_numerator_for_haplotype_i(
                    self.max_phase - 1
            ):
                return math.log10(self.bayes_numerator_for_favored_haplotype) - math.log10(
                    sum(
                        [self.bayes_numerator_for_haplotype_i(_i - 1) for _i in
                         range(1, self.ploidy_phase_set + 1) if
                         _i - 1 != self.max_phase - 1]
                    )
                )

    @property
    def posterior_probability_for_favored_haplotype(self) -> Union[None, str, float]:
        """
        # posterior_probability_haplotype_i = P(haplotype_i|aligned_segment)

        # aligned_segment.set_tag(tag = 'fp', value = str(phased_read.posterior_probability_for_haplotype_i(c)), value_type='Z',
        replace=True) # aligned_segment.set_tag(tag = 'pp', value = str(phased_read.posterior_probability_for_haplotype_i(int(
        aligned_segment.get_tag('oa')))), value_type='Z', replace=True)

        Returns:
            Union[None, str, float]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            if self.total_probability_of_read_given_haplotypes and self.bayes_numerator_for_haplotype_i(
                    self.max_phase - 1
            ):
                return self.bayes_numerator_for_haplotype_i(
                    self.max_phase - 1
                ) / self.total_probability_of_read_given_haplotypes

    @property
    def log_posterior_probability_for_favored_haplotype(self) -> Union[None, str, float]:
        """
        posterior_probability_haplotype_i = P(haplotype_i|aligned_segment)

        Returns:
            Union[None, str, float]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            if self.total_probability_of_read_given_haplotypes and self.bayes_numerator_for_haplotype_i(
                    self.max_phase - 1
            ):
                return math.log10(self.bayes_numerator_for_haplotype_i(self.max_phase - 1)) - math.log10(
                    self.total_probability_of_read_given_haplotypes
                )

    def bayes_numerator_for_haplotype_i(self, i: int) -> Union[None, str, float]:
        """
        P(aligned_segment|haplotype_i)P(haplotype_i)
        Bayes numerator. likelihood * prior

        Returns:
            Union[None, str, float]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return self.calculate_likelihood_of_read_given_haplotype_i(i - 1) * self.prior_probability_for_haplotype_i(
                i - 1
            )
        # if self.likelihood_for_haplotype_i(i) and self.prior_probability_for_haplotype_i(i):

    def log_likelihood_ratio_for_haplotype_i_vs_not_haplotype_i(self, i: int) -> Union[None, str, float]:
        """

        Args:
            i:

        Returns:
            Union[None, str, float]:

        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            if self.total_probability_of_read_given_haplotypes and self.bayes_numerator_for_haplotype_i(i - 1):
                return math.log10(self.bayes_numerator_for_haplotype_i(i - 1)) - math.log10(
                    sum(
                        [self.bayes_numerator_for_haplotype_i(_i - 1) for _i in
                         range(1, self.ploidy_phase_set + 1) if
                         _i - 1 != i - 1]
                    )
                )

    def posterior_probability_for_haplotype_i(self, i: int) -> Union[None, str, float]:
        """
        # posterior_probability_haplotype_i = P(haplotype_i|aligned_segment)

        # aligned_segment.set_tag(tag = 'fp', value = str(phased_read.posterior_probability_for_haplotype_i(c)), value_type='Z',
        replace=True) # aligned_segment.set_tag(tag = 'pp', value = str(phased_read.posterior_probability_for_haplotype_i(int(
        aligned_segment.get_tag('oa')))), value_type='Z', replace=True)

        Args:
            i:

        Returns:
            Union[None, str, float]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            if self.total_probability_of_read_given_haplotypes and self.bayes_numerator_for_haplotype_i(i - 1):
                return self.bayes_numerator_for_haplotype_i(i - 1) / self.total_probability_of_read_given_haplotypes

    def log_posterior_probability_for_haplotype_i(self, i: int) -> Union[None, str, float]:
        """
        posterior_probability_haplotype_i = P(haplotype_i|aligned_segment)

        Args:
            i:

        Returns:
            Union[None, str, float]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            if self.total_probability_of_read_given_haplotypes and self.bayes_numerator_for_haplotype_i(i - 1):
                return math.log10(self.bayes_numerator_for_haplotype_i(i - 1)) - math.log10(
                    self.total_probability_of_read_given_haplotypes
                )

    @property
    def total_probability_of_read_given_haplotypes(self) -> Union[None, str, float]:
        """
        total_probability_of_read_given_haplotypes = sum(P(aligned_segment|haplotype_i)P(haplotype_i)) for i = 1,...,ploidy Our
        model assumes that the haplotypes listed in the VCF file are the ground truth molecular composition of the
        populations from which these reads were sampled from physically.

        Returns:
            Union[None, str, float]:
        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return 'Nonphasable'
        else:
            return sum([self.bayes_numerator_for_haplotype_i(i) for i in range(1, self.ploidy_phase_set + 1)])


class SimulatedPhasedRead(PhasedRead):
    """

    """

    def __init__(self):
        PhasedRead.__init__(self)

    @property
    def is_phased_incorrectly(self) -> Union[None, str, bool]:
        """

        Returns:
            Union[None, str, bool]:

        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        else:
            if self.is_Phased:
                if self.aligned_segment.has_tag('ha'):
                    return str(self.phase) != str(self.aligned_segment.get_tag('ha'))

    @property
    def is_phased_correctly(self) -> object:
        """

        Returns:

        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        else:
            if self.is_Phased:
                if self.aligned_segment.has_tag('ha'):
                    return str(self.phase) == str(self.aligned_segment.get_tag('ha'))

    @property
    def matches_true_alignment(self) -> bool:
        """

        Returns:
            bool:

        """
        if self.aligned_segment.has_tag('ml'):
            return str(self.aligned_segment.get_tag('ml')) == 'mapping_match'

    @property
    def fraction_of_alignment_length_overlapping_true_alignment(self) -> object:
        """

        Returns:
            object:

        """
        if self.aligned_segment.has_tag('OV'):
            return str(self.aligned_segment.get_tag('OV'))

    @property
    def favored_phase_is_correct(self) -> Union[None, str, bool]:
        """

        Returns:
            Union[None, str, bool]:

        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        else:
            if self.one_phase_is_favored:
                if self.aligned_segment.has_tag('ha'):
                    return str(self.max_phase) == str(self.aligned_segment.get_tag('ha'))

    @property
    def favored_phase_is_incorrect(self) -> Union[None, str, bool]:
        """

        Returns:
            Union[None, str, bool]:

        """
        if self.Phase_Set_max is None:
            return
        elif self.Phase_Set_max == 'Nonphasable':
            return False
        else:
            if self.one_phase_is_favored:
                if self.aligned_segment.has_tag('ha'):
                    return str(self.max_phase) != str(self.aligned_segment.get_tag('ha'))

    @property
    def mapped_within_10percent_of_true_alignment(self) -> bool:
        """

        Returns:
            bool:

        """
        if self.aligned_segment.has_tag('ml'):
            return str(self.aligned_segment.get_tag('ml')) == 'within_10percent'

    @property
    def does_not_overlap_true_alignment_but_does_align_to_true_contig(self) -> bool:
        """

        Returns:
            bool:

        """
        if self.aligned_segment.has_tag('ml'):
            return str(self.aligned_segment.get_tag('ml')) == 'ref_match'

    @property
    def does_not_match_true_alignment(self) -> bool:
        """

        Returns:
            bool:

        """
        if self.aligned_segment.has_tag('ml'):
            return str(self.aligned_segment.get_tag('ml')) == 'non_match'

    @property
    def fraction_of_read_overlapping_true_alignment(self) -> object:
        """

        Returns:

        """
        if self.aligned_segment.has_tag('ov'):
            return str(self.aligned_segment.get_tag('ov'))

    @property
    def validation_using_true_alignment_label(self) -> str:
        """

        Returns:
            str:

        """
        if self.aligned_segment.has_tag('ml'):
            return str(self.aligned_segment.get_tag('ml'))

    @property
    def matches_true_alignment(self) -> bool:
        """

        Returns:
            bool:

        """
        if self.aligned_segment.has_tag('ml'):
            return str(self.aligned_segment.get_tag('ml')) == 'mapping_match'

    @property
    def mapped_within_10percent_of_true_alignment(self) -> bool:
        """

        Returns:
            bool:

        """
        if self.aligned_segment.has_tag('ml'):
            return str(self.aligned_segment.get_tag('ml')) == 'within_10percent'

    @property
    def does_not_overlap_true_alignment_but_does_align_to_true_contig(self) -> bool:
        """

        Returns:
            bool:

        """
        if self.aligned_segment.has_tag('ml'):
            return str(self.aligned_segment.get_tag('ml')) == 'ref_match'

    @property
    def does_not_match_true_alignment(self) -> bool:
        """

        Returns:
            bool:

        """
        if self.aligned_segment.has_tag('ml'):
            return str(self.aligned_segment.get_tag('ml')) == 'non_match'
