from collections import namedtuple
from mmsplice.vcf_dataloader import SplicingVCFDataloader, FastaSeq

from conftest import gtf_file, fasta_file, snps, deletions, \
    insertions, variants


def test_FastSeq_getSeq():
    IV = namedtuple('iv', 'chrom start end strand')
    fasta = FastaSeq(fasta_file)

    iv = IV(chrom='17', start=41267742, end=41267752, strand='+')
    seq = fasta.getSeq(iv)
    assert seq == 'CTTGCAAAATA'

    iv = IV(chrom='17', start=41267742, end=41267752, strand='-')
    seq = fasta.getSeq(iv)
    assert seq == 'TATTTTGCAAG'


def test_splicing_vcf_loads_all(vcf_path):
    dl = SplicingVCFDataloader(gtf_file, fasta_file, vcf_path)
    assert sum(1 for i in dl) == len(variants) - 1


def test_splicing_vcf_loads_snps(vcf_path):
    dl = SplicingVCFDataloader(gtf_file, fasta_file, vcf_path)

    expected_snps_seq = [
        {
            'seq':
            'CAAATCTTAAATTTACTTTATTTTAAAATGATAAAATGAAGTTGTCATTT'
            'TATAAACCTTTTAAAAAGATATATATATATGTTTTTCTAATGTGTTAAAG'
            'TTCATTGGAACAGAAAGAAATGGATTTATCTGCTCTTCGCGTTGAAGAAG'
            'TACAAAATGTCATTAATGCTATGCAGAAAATCTTAGAGTGTCCCATCTGG'
            'TAAGTCAGCACAAGAGTGTATTAATTTGGGATTCCTATGATTATCTCCTA'
            'TGCAAATGAACAGAATTGACCTTACATACTAGGGAAGAAAAGACATGTC',

            'alt_seq':
            'CAAATCTTAAATTTACTTTATTTTAAAATGATAAAATGAAGTTGTCATTT'
            'TATAAACCTTTTAAAAAGATATATATATATGTTTTTCTAATGTGTTAAAG'
            'TTCATTGGAACAGAAAGAAATGGATTTATCTGCTCTTCGCGTTGAAGAAG'
            'TACAAAATGTCATTAATGCTATGCAGAAAATCTTAGAGTGTCCCATCTGC'
            'TAAGTCAGCACAAGAGTGTATTAATTTGGGATTCCTATGATTATCTCCTA'
            'TGCAAATGAACAGAATTGACCTTACATACTAGGGAAGAAAAGACATGTC'
        },
        {
            'seq':
            'CAAATCTTAAATTTACTTTATTTTAAAATGATAAAATGAAGTTGTCATTT'
            'TATAAACCTTTTAAAAAGATATATATATATGTTTTTCTAATGTGTTAAAG'
            'TTCATTGGAACAGAAAGAAATGGATTTATCTGCTCTTCGCGTTGAAGAAG'
            'TACAAAATGTCATTAATGCTATGCAGAAAATCTTAGAGTGTCCCATCTGG'
            'TAAGTCAGCACAAGAGTGTATTAATTTGGGATTCCTATGATTATCTCCTA'
            'TGCAAATGAACAGAATTGACCTTACATACTAGGGAAGAAAAGACATGTC',

            'alt_seq':
            'CAAATCTTAAATTTACTTTATTTTAAAATGATAAAATGAAGTTGTCATTT'
            'TATAAACCTTTTAAAAAGATATATATATATGTTTTTCTAATGTGTTAAAG'
            'TTCATTGGAACAGAAAGAAATGGATTTATCTGCTCTTCGCGTTGAAGAAG'
            'TACAAAATGTCATTAATGCTATGCAGAAAATCTTAGAGTGTCCCATCTGG'
            'TAAGTCAGCACAAGAGTGTATTAATTTGGGATTCCTATGATTATCTCCTA'
            'TGCAAATGAACAGAATTGACCTTACATACTAGGGAAGAAAAGACATGTC',
        }
    ]

    for i in range(len(snps)):
        d = next(dl)
        print(d)
        print(d['metadata']['ExonInterval']['start'])
        print(d['metadata']['ExonInterval']['end'])
        assert d['inputs']['seq'] == expected_snps_seq[i]['seq']
        assert d['inputs_mut']['seq'] == expected_snps_seq[i]['alt_seq']


def test_splicing_vcf_loads_deletions(vcf_path):
    dl = SplicingVCFDataloader(gtf_file, fasta_file, vcf_path)

    expected_snps_seq = [
        {
            'seq':
            'TAACAGCTCAAAGTTGAACTTATTCACTAAGAATAGCTTTATTTTTAAATA'
            'AATTATTGAGCCTCATTTATTTTCTTTTTCTCCCCCCCTACCCTGCTAGTC'
            'TGGAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCA'
            'AGTAAGTTTGAATGTGTTATGTGGCTCCATTATTAGCTTTTGTTTTTGTCC'
            'TTCATAACCCAGGAAACACCTAACTTTATAGAAGCTTTACTTTCTTCAAT',
            'alt_seq':
            'TAACAGCTCAAAGTTGAACTTATTCACTAAGAATAGCTTTATTTTTAAATA'
            'AATTATTGAGCCTCATTTATTTTCTTTTTCTCCCCCCCTACCCTGCTAGTC'
            'TGGAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCG'
            'TAAGTTTGAATGTGTTATGTGGCTCCATTATTAGCTTTTGTTTTTGTCCTT'
            'CATAACCCAGGAAACACCTAACTTTATAGAAGCTTTACTTTCTTCAAT'
        },
        {
            'seq':
            'TAACAGCTCAAAGTTGAACTTATTCACTAAGAATAGCTTTATTTTTAAATA'
            'AATTATTGAGCCTCATTTATTTTCTTTTTCTCCCCCCCTACCCTGCTAGTC'
            'TGGAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCA'
            'AGTAAGTTTGAATGTGTTATGTGGCTCCATTATTAGCTTTTGTTTTTGTCC'
            'TTCATAACCCAGGAAACACCTAACTTTATAGAAGCTTTACTTTCTTCAAT',
            'alt_seq':
            'TAACAGCTCAAAGTTGAACTTATTCACTAAGAATAGCTTTATTTTTAAATA'
            'AATTATTGAGCCTCATTTATTTTCTTTTTCTCCCCCCCTACCCTGCTAGTC'
            'TGGAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCG'
            'TAAGTTTGAATGTGTTATGTGGCTCCATTATTAGCTTTTGTTTTTGTCCTT'
            'CATAACCCAGGAAACACCTAACTTTATAGAAGCTTTACTTTCTTCAAT'
        },
        {
            'seq':
            'TAACAGCTCAAAGTTGAACTTATTCACTAAGAATAGCTTTATTTTTAAATA'
            'AATTATTGAGCCTCATTTATTTTCTTTTTCTCCCCCCCTACCCTGCTAGTC'
            'TGGAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCA'
            'AGTAAGTTTGAATGTGTTATGTGGCTCCATTATTAGCTTTTGTTTTTGTCC'
            'TTCATAACCCAGGAAACACCTAACTTTATAGAAGCTTTACTTTCTTCAAT',
            'alt_seq':
            'TAACAGCTCAAAGTTGAACTTATTCACTAAGAATAGCTTTATTTTTAAATA'
            'AATTATTGAGCCTCATTTATTTTCTTTTTCTCCCCCCCTACCCTGCTAGTC'
            'TGGAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCT'
            'AGTTTGAATGTGTTATGTGGCTCCATTATTAGCTTTTGTTTTTGTCCTTCA'
            'TAACCCAGGAAACACCTAACTTTATAGAAGCTTTACTTTCTTCAATTAAG'
        },
        {
            'seq':
            'TAACAGCTCAAAGTTGAACTTATTCACTAAGAATAGCTTTATTTTTAAATA'
            'AATTATTGAGCCTCATTTATTTTCTTTTTCTCCCCCCCTACCCTGCTAGTC'
            'TGGAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCA'
            'AGTAAGTTTGAATGTGTTATGTGGCTCCATTATTAGCTTTTGTTTTTGTCC'
            'TTCATAACCCAGGAAACACCTAACTTTATAGAAGCTTTACTTTCTTCAAT',
            'alt_seq':
            'ATAACAGCTCAAAGTTGAACTTATTCACTAAGAATAGCTTTATTTTTAAAT'
            'AAATTATTGAGCCTCATTTATTTTCTTTTTCTCCCCCCCTACCCTGCTATC'
            'TGGAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCA'
            'AGTAAGTTTGAATGTGTTATGTGGCTCCATTATTAGCTTTTGTTTTTGTCC'
            'TTCATAACCCAGGAAACACCTAACTTTATAGAAGCTTTACTTTCTTCAAT'
        },
        {
            'seq':
            'TAACAGCTCAAAGTTGAACTTATTCACTAAGAATAGCTTTATTTTTAAATA'
            'AATTATTGAGCCTCATTTATTTTCTTTTTCTCCCCCCCTACCCTGCTAGTC'
            'TGGAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCA'
            'AGTAAGTTTGAATGTGTTATGTGGCTCCATTATTAGCTTTTGTTTTTGTCC'
            'TTCATAACCCAGGAAACACCTAACTTTATAGAAGCTTTACTTTCTTCAAT',
            'alt_seq':
            'CATAACAGCTCAAAGTTGAACTTATTCACTAAGAATAGCTTTATTTTTAAA'
            'TAAATTATTGAGCCTCATTTATTTTCTTTTTCTCCCCCCCTACCCTGCTTC'
            'TGGAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCA'
            'AGTAAGTTTGAATGTGTTATGTGGCTCCATTATTAGCTTTTGTTTTTGTCC'
            'TTCATAACCCAGGAAACACCTAACTTTATAGAAGCTTTACTTTCTTCAAT'
        },
        {
            'seq':
            'TAACAGCTCAAAGTTGAACTTATTCACTAAGAATAGCTTTATTTTTAAATA'
            'AATTATTGAGCCTCATTTATTTTCTTTTTCTCCCCCCCTACCCTGCTAGTC'
            'TGGAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCA'
            'AGTAAGTTTGAATGTGTTATGTGGCTCCATTATTAGCTTTTGTTTTTGTCC'
            'TTCATAACCCAGGAAACACCTAACTTTATAGAAGCTTTACTTTCTTCAAT',
            'alt_seq':
            'TAACAGCTCAAAGTTGAACTTATTCACTAAGAATAGCTTTATTTTTAAATA'
            'AATTATTGAGCCTCATTTATTTTCTTTTTCTCCCCCCCTACCCTGCTAGCT'
            'GGAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCAA'
            'GTAAGTTTGAATGTGTTATGTGGCTCCATTATTAGCTTTTGTTTTTGTCCT'
            'TCATAACCCAGGAAACACCTAACTTTATAGAAGCTTTACTTTCTTCAAT'
        },
        {
            'seq':
            'TAACAGCTCAAAGTTGAACTTATTCACTAAGAATAGCTTTATTTTTAAATA'
            'AATTATTGAGCCTCATTTATTTTCTTTTTCTCCCCCCCTACCCTGCTAGTC'
            'TGGAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCA'
            'AGTAAGTTTGAATGTGTTATGTGGCTCCATTATTAGCTTTTGTTTTTGTCC'
            'TTCATAACCCAGGAAACACCTAACTTTATAGAAGCTTTACTTTCTTCAAT',
            'alt_seq':
            'TAACAGCTCAAAGTTGAACTTATTCACTAAGAATAGCTTTATTTTTAAATA'
            'AATTATTGAGCCTCATTTATTTTCTTTTTCTCCCCCCCTACCCTGCTAGGT'
            'AAGTTTGAATGTGTTATGTGGCTCCATTATTAGCTTTTGTTTTTGTCCTTC'
            'ATAACCCAGGAAACACCTAACTTTATAGAAGCTTTACTTTCTTCAAT'
        }
    ]

    for i in range(len(snps)):
        d = next(dl)

    for i in range(len(deletions) - 1):
        d = next(dl)

        print('Variant position:', d['metadata']['variant']['POS'])
        print('Interval:',
              d['metadata']['ExonInterval']['start'],
              '-',
              d['metadata']['ExonInterval']['end'])
        print(d)
        assert d['inputs']['seq'] == expected_snps_seq[i]['seq']
        assert d['inputs_mut']['seq'] == expected_snps_seq[i]['alt_seq']


def test_splicing_vcf_loads_insertions(vcf_path):
    dl = SplicingVCFDataloader(gtf_file, fasta_file, vcf_path)

    for i in range(len(snps) + len(deletions) - 1):
        d = next(dl)

    expected_snps_seq = [
        {
            'seq':
            'CAAATCTTAAATTTACTTTATTTTAAAATGATAAAATGAAGTTGTCATTTTA'
            'TAAACCTTTTAAAAAGATATATATATATGTTTTTCTAATGTGTTAAAGTTCA'
            'TTGGAACAGAAAGAAATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAA'
            'ATGTCATTAATGCTATGCAGAAAATCTTAGAGTGTCCCATCTGGTAAGTCAG'
            'CACAAGAGTGTATTAATTTGGGATTCCTATGATTATCTCCTATGCAAATGAA'
            'CAGAATTGACCTTACATACTAGGGAAGAAAAGACATGTC',
            'alt_seq':
            'CAAATCTTAAATTTACTTTATTTTAAAATGATAAAATGAAGTTGTCATTTTA'
            'TAAACCTTTTAAAAAGATATATATATATGTTTTTCTAATGTGTTAAAGTTCA'
            'TTGGAACAGAAAGAAATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAA'
            'ATGTCATTAATGCTATGCAGAAAATCTTAGAGTGTCCCATCTGCATCTGGTA'
            'AGTCAGCACAAGAGTGTATTAATTTGGGATTCCTATGATTATCTCCTATGCA'
            'AATGAACAGAATTGACCTTACATACTAGGGAAGAAAAGACATGTC'
        },
        {
            'seq':
            'CAAATCTTAAATTTACTTTATTTTAAAATGATAAAATGAAGTTGTCATTTTA'
            'TAAACCTTTTAAAAAGATATATATATATGTTTTTCTAATGTGTTAAAGTTCA'
            'TTGGAACAGAAAGAAATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAA'
            'ATGTCATTAATGCTATGCAGAAAATCTTAGAGTGTCCCATCTGGTAAGTCAG'
            'CACAAGAGTGTATTAATTTGGGATTCCTATGATTATCTCCTATGCAAATGAA'
            'CAGAATTGACCTTACATACTAGGGAAGAAAAGACATGTC',
            'alt_seq':
            'CAAATCTTAAATTTACTTTATTTTAAAATGATAAAATGAAGTTGTCATTTTA'
            'TAAACCTTTTAAAAAGATATATATATATGTTTTTCTAATGTGTTAAAGTTCA'
            'TTGGAACAGAAAGAAATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAA'
            'ATGTCATTAATGCTATGCAGAAAATCTTAGAGTGTCCCATCTGTGGTAAGTC'
            'AGCACAAGAGTGTATTAATTTGGGATTCCTATGATTATCTCCTATGCAAATG'
            'AACAGAATTGACCTTACATACTAGGGAAGAAAAGACATGTC'
        },
        {
            'seq':
            'TAACAGCTCAAAGTTGAACTTATTCACTAAGAATAGCTTTATTTTTAAATAA'
            'ATTATTGAGCCTCATTTATTTTCTTTTTCTCCCCCCCTACCCTGCTAGTCTG'
            'GAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCAAGT'
            'AAGTTTGAATGTGTTATGTGGCTCCATTATTAGCTTTTGTTTTTGTCCTTCA'
            'TAACCCAGGAAACACCTAACTTTATAGAAGCTTTACTTTCTTCAAT',
            'alt_seq':
            'ACAGCTCAAAGTTGAACTTATTCACTAAGAATAGCTTTATTTTTAAATAAAT'
            'TATTGAGCCTCATTTATTTTCTTTTTCTCCCCCCCTACCCTGCTAGTTTCTG'
            'GAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCAAGT'
            'AAGTTTGAATGTGTTATGTGGCTCCATTATTAGCTTTTGTTTTTGTCCTTCA'
            'TAACCCAGGAAACACCTAACTTTATAGAAGCTTTACTTTCTTCAAT'
        },
        {
            'seq':
            'TAACAGCTCAAAGTTGAACTTATTCACTAAGAATAGCTTTATTTTTAAATAA'
            'ATTATTGAGCCTCATTTATTTTCTTTTTCTCCCCCCCTACCCTGCTAGTCTG'
            'GAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCAAGT'
            'AAGTTTGAATGTGTTATGTGGCTCCATTATTAGCTTTTGTTTTTGTCCTTCA'
            'TAACCCAGGAAACACCTAACTTTATAGAAGCTTTACTTTCTTCAAT',
            'alt_seq':
            'ACAGCTCAAAGTTGAACTTATTCACTAAGAATAGCTTTATTTTTAAATAAAT'
            'TATTGAGCCTCATTTATTTTCTTTTTCTCCCCCCCTACCCTGCTTTAGTCTG'
            'GAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCAAGT'
            'AAGTTTGAATGTGTTATGTGGCTCCATTATTAGCTTTTGTTTTTGTCCTTCA'
            'TAACCCAGGAAACACCTAACTTTATAGAAGCTTTACTTTCTTCAAT'
        },
        {
            'seq': 'CAAATCTTAAATTTACTTTATTTTAAAATGATAAAATGAAGTTGT'
            'CATTTTATAAACCTTTTAAAAAGATATATATATATGTTTTTCTAATGTGTTA'
            'AAGTTCATTGGAACAGAAAGAAATGGATTTATCTGCTCTTCGCGTTGAAGAA'
            'GTACAAAATGTCATTAATGCTATGCAGAAAATCTTAGAGTGTCCCATCTGGT'
            'AAGTCAGCACAAGAGTGTATTAATTTGGGATTCCTATGATTATCTCCTATGC'
            'AAATGAACAGAATTGACCTTACATACTAGGGAAGAAAAGACATGTC',
            'alt_seq': 'AATCTTAAATTTACTTTATTTTAAAATGATAAAATGAAG'
            'TTGTCATTTTATAAACCTTTTAAAAAGATATATATATATGTTTTTCTAATGT'
            'GTTAAAGAGTTCATTGGAACAGAAAGAAATGGATTTATCTGCTCTTCGCGTT'
            'GAAGAAGTACAAAATGTCATTAATGCTATGCAGAAAATCTTAGAGTGTCCCA'
            'TCTGGTAAGTCAGCACAAGAGTGTATTAATTTGGGATTCCTATGATTATCTC'
            'CTATGCAAATGAACAGAATTGACCTTACATACTAGGGAAGAAAAGACATGTC'
        }
    ]

    for i in range(len(insertions)):
        d = next(dl)

        print(d)
        print(d['metadata']['ExonInterval']['start'])
        print(d['metadata']['ExonInterval']['end'])
        assert d['inputs']['seq'] == expected_snps_seq[i]['seq']
        assert d['inputs_mut']['seq'] == expected_snps_seq[i]['alt_seq']
