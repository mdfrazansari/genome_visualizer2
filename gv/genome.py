# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 13:40:29 2018

@author: fraz
"""

import allel
import numpy as np
from Bio import SeqIO
from pyfaidx import Fasta, wrap_sequence

STANDARD_GENOME_PATH = "F:/RG/intern/genome_visualizer/"

class Genome():
    fastaFileName = ""

    def __init__(self, fileName):
        self.fastaFileName = fileName
    
    def splitGenome(self):
        fa= Fasta(self.fastaFileName)
        for seq in fa:
            with open('{}{}.fa'.format(STANDARD_GENOME_PATH, seq.name), 'w') as out:
                out.write('>{}\n'.format(seq.name))
                for line in wrap_sequence(70, str(seq)):
                    out.write(line)
        print("<<<<<<<Splitted>>>>>>")
        
class Chromosome():
    def __init__(self, chromosome_name):
        if(chromosome_name in VCF.VCF_CHROMOSOMES): # check valid name
            chromosomeFile = '{}{}.{}'.format(STANDARD_GENOME_PATH, chromosome_name, 'fa')
            with open(chromosomeFile) as chromosomeData:  # Will close handle cleanly
                lengths = []
                for record in SeqIO.parse(chromosomeData, "fasta"):  # (generator)...in this case it is not a multi fasta file
                    lengths.append(record.seq)
            self.recordSequence = record.seq
    def getLength(self):
        return len(str(self.recordSequence))
        
class VCF():
    vcfFileName = ""
    VCF_CHROMOSOMES = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7',
                       'chr8', 'chr9', 'chr10', 'chr11', 'chr12', 'chr13',
                       'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19',
                       'chr20', 'chr21', 'chr22', 'chrX', 'chrY']
    
    def __init__(self, fileName):
        self.vcfFileName = fileName;
        # AVAILABLE FIELDS
        # 'CHROM', 'POS', 'ID', 'REF', 'ALT_1', 'ALT_2', 'ALT_3', 'QUAL', 'PRO',
#       'EPP_1', 'EPP_2', 'EPP_3', 'SRF', 'NS', 'AB_1', 'AB_2', 'AB_3',
#       'NUMALT', 'SRR', 'RPPR', 'QA_1', 'QA_2', 'QA_3', 'RUN_1', 'RUN_2',
#       'RUN_3', 'MQM_1', 'MQM_2', 'MQM_3', 'DPB', 'PAIREDR', 'SAR_1', 'SAR_2',
#       'SAR_3', 'DPRA_1', 'DPRA_2', 'DPRA_3', 'BVAR', 'DP', 'RO', 'GTI',
#       'ODDS', 'AC_1', 'AC_2', 'AC_3', 'AF_1', 'AF_2', 'AF_3', 'PAO_1',
#       'PAO_2', 'PAO_3', 'PAIRED_1', 'PAIRED_2', 'PAIRED_3', 'CIGAR_1',
#       'CIGAR_2', 'CIGAR_3', 'PQR', 'AO_1', 'AO_2', 'AO_3', 'LEN_1', 'LEN_2',
#       'LEN_3', 'SRP', 'ABP_1', 'ABP_2', 'ABP_3', 'RPP_1', 'RPP_2', 'RPP_3',
#       'MEANALT_1', 'MEANALT_2', 'MEANALT_3', 'AN', 'MQMR', 'QR', 'SAP_1',
#       'SAP_2', 'SAP_3', 'PQA_1', 'PQA_2', 'PQA_3', 'TYPE_1', 'TYPE_2',
#       'TYPE_3', 'EPPR', 'SAF_1', 'SAF_2', 'SAF_3', 'FILTER_PASS', 'numalt',
#       'svlen_1', 'svlen_2', 'svlen_3', 'is_snp'
        self.dataFrame = allel.vcf_to_dataframe(fileName, fields='*')
        
    def getFileName(self):
        return self.vcfFileName
        
    def getVariation(self, chromosome_name):
        return self.dataFrame.POS[self.dataFrame.CHROM == chromosome_name]

    def getVariationAllDetails(self, chromosome_name):
        return self.dataFrame[self.dataFrame.CHROM == chromosome_name]


