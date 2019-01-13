# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 21:01:27 2018

@author: fraz
"""
import pandas as pd


class Census():
    censusFile = ""

    def __init__(self, file):
        self.censusFile = file
        self.census_data = pd.read_csv(self.censusFile)
        self.gene_location = self.census_data['Genome Location']

    def getChromosomeCensusData(self, chromosomeName):
        data = self.gene_location[self.gene_location.str.startswith(chromosomeName + ':')]
        return self.census_data.iloc[data.index]
