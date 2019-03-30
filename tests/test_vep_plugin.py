import os.path
import pytest
from mmsplice.vcf_dataloader import SplicingVCFDataloader
from mmsplice import MMSplice, predict_all_table
from mmsplice.utils import read_vep, max_varEff
from scipy.stats import pearsonr


vep_output = 'variant_effect_output.txt'

@pytest.mark.skipif(not os.path.isfile(vep_output),
                    reason="No vep result file to test")
def test_vep_plugin():
    gtf = 'tests/data/test.gtf'
    vcf = 'tests/data/test.vcf.gz'
    fasta = 'tests/data/hg19.nochr.chr17.fa'
    gtfIntervalTree = 'tests/data/test.pkl'  # pickle exon interval Tree

    dl = SplicingVCFDataloader(gtfIntervalTree,
                               fasta,
                               vcf,
                               out_file=gtfIntervalTree,
                               split_seq=False, overhang=(100, 100))

    model = MMSplice(
        exon_cut_l=0,
        exon_cut_r=0,
        acceptor_intron_cut=6,
        donor_intron_cut=6,
        acceptor_intron_len=50,
        acceptor_exon_len=3,
        donor_exon_len=5,
        donor_intron_len=13)

    df_python = predict_all_table(model, dl, batch_size=1024,
                                  split_seq=False, assembly=True,
                                  pathogenicity=True, splicing_efficiency=True)
    df_python_predictionsMax = max_varEff(df_python).set_index('ID')

    df_plugin = read_vep(vep_output)
    df_plugin_predictionsMax = max_varEff(df_plugin).set_index('ID')

    indexes = list(set(df_plugin_predictionsMax.index) &
                   set(df_python_predictionsMax.index))

    vep_plugin_dlogitPsi = df_plugin_predictionsMax.loc[indexes,
                                                        'mmsplice_dlogitPsi']
    python_package = df_python_predictionsMax.loc[indexes,
                                                  'mmsplice_dlogitPsi']

    assert pearsonr(vep_plugin_dlogitPsi, python_package)[0] >= 0.99
