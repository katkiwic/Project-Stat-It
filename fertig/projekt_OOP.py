# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 17:23:36 2017

@author: buehr
"""

import pandas as pd

class DataFrame:
    def __init__(self, filename):
        self._filename = filename
        self._df = pd.DataFrame.from_csv(self._filename, index_col = 0)
        self._df['index'] = [int(y) for y in list(self._df.index.year)]
        self._df = self._df.set_index('index')

    def get_filename(self):
        return self._filename
    
    def get_years_list(self):
        return sorted([str(y) for y in list(pd.unique(self._df.index))])
    
class Naturalizations(DataFrame):
    def __init__(self, filename):
        DataFrame.__init__(self, filename)
    
    def get_countries_list(self):
        return sorted(list(pd.unique(self._df.iloc[:, 0].values)))
    
    def get_continents_list(self):
        return sorted(list(pd.unique(self._df.iloc[:, 1].values)))
    
    def get_sexes_list(self):   
        return sorted(list(pd.unique(self._df.iloc[:, 2].values)))
    
    def get_age_classes_list(self):    
        return sorted(list(pd.unique(self._df.iloc[:, 3].values)))

class Crimes(DataFrame):
    def __init__(self, filename):
        DataFrame.__init__(self, filename)
    
    def get_crime_cats_list(self):
        return list(pd.unique(self._df.columns[1:].values))
