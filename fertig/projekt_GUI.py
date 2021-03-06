# -*- coding: utf-8 -*-
'''
Created on Fri Apr  7 10:41:21 2017

@author: buehr
'''

from PyQt5 import QtWidgets, QtCore
from projekt_OOP import Naturalizations, Crimes
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import sys

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle('Statistik')
        
        self.einbuergerungen = Naturalizations('einbuergerungen.csv')
        self.straftaten = Crimes('straftaten.csv')
        self.df1 = None
        self.df2 = None
        self.df_status = [False, False]
        
        # (1) top
        self.lab_jahr = QtWidgets.QLabel('Jahr')
        self.lab_jahr.setFixedWidth(90)
        
        self.qlist_jahre = QtWidgets.QListWidget()
        self.qlist_jahre.setMaximumHeight(50)
        self.qlist_jahre.addItems(['(Alle)'] + self.straftaten.get_years_list())
        self.qlist_jahre.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.qlist_jahre.setCurrentRow(0)
        self.qlist_jahre.itemSelectionChanged.connect(self.create_df1)
        self.qlist_jahre.itemSelectionChanged.connect(self.create_df2)
        
        self.h1_1 = QtWidgets.QHBoxLayout()
        self.h1_1.addWidget(self.lab_jahr)
        self.h1_1.setAlignment(QtCore.Qt.AlignTop)
        self.h1_2 = QtWidgets.QHBoxLayout()
        self.h1_2.addWidget(self.qlist_jahre)
        self.h1_2.setAlignment(QtCore.Qt.AlignTop)   
        self.h1_3 = QtWidgets.QHBoxLayout()
        self.h1_3.addLayout(self.h1_1)
        self.h1_3.addLayout(self.h1_2)
        self.h1_3.setAlignment(QtCore.Qt.AlignTop)
        
        self.g_box1_1 = QtWidgets.QGroupBox('Allgemeines')
        self.g_box1_1.setLayout(self.h1_3)
        
        # middle left (2)
        self.lab_dateiname1 = QtWidgets.QLabel('Dateiname: ')
        self.lab_dateiname1.setFixedWidth(90)
        self.qline_dateiname1 = QtWidgets.QLineEdit()
        self.qline_dateiname1.setReadOnly(True)
        self.qline_dateiname1.setText(self.einbuergerungen.get_filename())
        
        self.radio_but_land = QtWidgets.QRadioButton('Land')      
        self.radio_but_land.setFixedWidth(90)
        self.radio_but_land.setChecked(True)
        self.radio_but_land.toggled.connect(self.radio_but_land_toggled)
        self.radio_but_kontinent = QtWidgets.QRadioButton('Kontinent')
        self.radio_but_kontinent.setFixedWidth(90)
        
        self.lab_geschlecht = QtWidgets.QLabel('Geschlecht')
        self.lab_geschlecht.setFixedWidth(90)
        self.lab_altersklasse = QtWidgets.QLabel('Altersklasse')
        self.lab_altersklasse.setFixedWidth(90)
        
        self.qlist_land = QtWidgets.QListWidget()
        self.qlist_land.setMaximumHeight(50)
        self.qlist_land.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.qlist_land.addItems(['(Alle)'] + self.einbuergerungen.get_countries_list())
        self.qlist_land.setCurrentRow(0)
        self.qlist_land.itemSelectionChanged.connect(self.create_df1)
        self.qlist_kontinent = QtWidgets.QListWidget()
        self.qlist_kontinent.setMaximumHeight(50)
        self.qlist_kontinent.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.qlist_kontinent.addItems(['(Alle)'] + self.einbuergerungen.get_continents_list())
        self.qlist_kontinent.setCurrentRow(0)
        self.qlist_kontinent.setEnabled(False)
        self.qlist_kontinent.itemSelectionChanged.connect(self.create_df1)
        self.qlist_geschlecht = QtWidgets.QListWidget()
        self.qlist_geschlecht.setMaximumHeight(50)
        self.qlist_geschlecht.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.qlist_geschlecht.addItems(['(Alle)'] + self.einbuergerungen.get_sexes_list())
        self.qlist_geschlecht.setCurrentRow(0)
        self.qlist_geschlecht.itemSelectionChanged.connect(self.create_df1)
        self.qlist_altersklasse = QtWidgets.QListWidget()
        self.qlist_altersklasse.setMaximumHeight(50)
        self.qlist_altersklasse.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.qlist_altersklasse.addItems(['(Alle)'] + self.einbuergerungen.get_age_classes_list())
        self.qlist_altersklasse.setCurrentRow(0)
        self.qlist_altersklasse.itemSelectionChanged.connect(self.create_df1)
        
        self.lab_durchschnitt1 = QtWidgets.QLabel('Durchschnitt')
        self.lab_durchschnitt1.setFixedWidth(90)
        self.lab_max1 = QtWidgets.QLabel('Maximum')
        self.lab_max1.setFixedWidth(90)
        self.lab_min1 = QtWidgets.QLabel('Minimum')
        self.lab_min1.setFixedWidth(90)
        self.lab_sa1 = QtWidgets.QLabel('S.abweichung')
        self.lab_sa1.setFixedWidth(90)
        
        self.qline_durchschnitt1 = QtWidgets.QLineEdit()
        self.qline_durchschnitt1.setAlignment(QtCore.Qt.AlignRight)
        self.qline_durchschnitt1.setReadOnly(True)
        self.qline_max1 = QtWidgets.QLineEdit()
        self.qline_max1.setAlignment(QtCore.Qt.AlignRight)
        self.qline_max1.setReadOnly(True)
        self.qline_min1 = QtWidgets.QLineEdit()
        self.qline_min1.setAlignment(QtCore.Qt.AlignRight)
        self.qline_min1.setReadOnly(True)
        self.qline_sa1 = QtWidgets.QLineEdit()
        self.qline_sa1.setAlignment(QtCore.Qt.AlignRight)
        self.qline_sa1.setReadOnly(True)
       
        self.but_graph1 = QtWidgets.QPushButton('Zeige Entwicklung')
        self.but_graph1.setFixedWidth(100)
        self.but_graph1.clicked.connect(self.but_graph1_clicked)
                
        self.h2_1 = QtWidgets.QHBoxLayout()
        self.h2_1.addWidget(self.lab_dateiname1)
        self.h2_1.addWidget(self.qline_dateiname1)
        
        self.h2_2 = QtWidgets.QHBoxLayout()
        self.h2_2.addWidget(self.radio_but_land)
        self.h2_2.setAlignment(QtCore.Qt.AlignTop)     
        self.h2_3 = QtWidgets.QHBoxLayout()
        self.h2_3.addWidget(self.qlist_land)
        self.h2_3.setAlignment(QtCore.Qt.AlignTop)        
        self.h2_4 = QtWidgets.QHBoxLayout()
        self.h2_4.addLayout(self.h2_2)
        self.h2_4.addLayout(self.h2_3)
        self.h2_4.setAlignment(QtCore.Qt.AlignTop)  
        
        self.h2_5 = QtWidgets.QHBoxLayout()
        self.h2_5.addWidget(self.radio_but_kontinent)
        self.h2_5.setAlignment(QtCore.Qt.AlignTop)
        self.h2_6 = QtWidgets.QHBoxLayout()
        self.h2_6.addWidget(self.qlist_kontinent)
        self.h2_6.setAlignment(QtCore.Qt.AlignTop)
        self.h2_7 = QtWidgets.QHBoxLayout()
        self.h2_7.addLayout(self.h2_5)
        self.h2_7.addLayout(self.h2_6)
        self.h2_7.setAlignment(QtCore.Qt.AlignTop)
        
        self.h2_8 = QtWidgets.QHBoxLayout()
        self.h2_8.addWidget(self.lab_geschlecht)
        self.h2_8.setAlignment(QtCore.Qt.AlignTop)
        self.h2_9 = QtWidgets.QHBoxLayout()        
        self.h2_9.addWidget(self.qlist_geschlecht)
        self.h2_9.setAlignment(QtCore.Qt.AlignTop)
        self.h2_10 = QtWidgets.QHBoxLayout()
        self.h2_10.addLayout(self.h2_8)
        self.h2_10.addLayout(self.h2_9)
        self.h2_10.setAlignment(QtCore.Qt.AlignTop)
        
        self.h2_11 = QtWidgets.QHBoxLayout()
        self.h2_11.addWidget(self.lab_altersklasse)
        self.h2_11.setAlignment(QtCore.Qt.AlignTop)
        self.h2_12 = QtWidgets.QHBoxLayout()        
        self.h2_12.addWidget(self.qlist_altersklasse)
        self.h2_12.setAlignment(QtCore.Qt.AlignTop)
        self.h2_13 = QtWidgets.QHBoxLayout()
        self.h2_13.addLayout(self.h2_11)
        self.h2_13.addLayout(self.h2_12)
        self.h2_13.setAlignment(QtCore.Qt.AlignTop)
        
        self.h2_14 = QtWidgets.QHBoxLayout()
        self.h2_14.addWidget(self.lab_durchschnitt1)
        self.h2_14.addWidget(self.qline_durchschnitt1)
        self.h2_14.setAlignment(QtCore.Qt.AlignTop)
        
        self.h2_15 = QtWidgets.QHBoxLayout()
        self.h2_15.addWidget(self.lab_max1)
        self.h2_15.addWidget(self.qline_max1)
        self.h2_15.setAlignment(QtCore.Qt.AlignTop)
        
        self.h2_16 = QtWidgets.QHBoxLayout()
        self.h2_16.addWidget(self.lab_min1)
        self.h2_16.addWidget(self.qline_min1)
        self.h2_16.setAlignment(QtCore.Qt.AlignTop)
        
        self.h2_17 = QtWidgets.QHBoxLayout()
        self.h2_17.addWidget(self.lab_sa1)
        self.h2_17.addWidget(self.qline_sa1)
        self.h2_17.setAlignment(QtCore.Qt.AlignTop)
        
        self.h2_18 = QtWidgets.QHBoxLayout()
        self.h2_18.addWidget(self.but_graph1)
        self.h2_18.setAlignment(QtCore.Qt.AlignRight)
                
        self.v2_1 = QtWidgets.QVBoxLayout()
        self.v2_1.addLayout(self.h2_1)
        self.v2_1.addLayout(self.h2_4)
        self.v2_1.addLayout(self.h2_7)
        self.v2_1.addLayout(self.h2_10)
        self.v2_1.addLayout(self.h2_13)
        self.v2_1.addLayout(self.h2_14)
        self.v2_1.addLayout(self.h2_15)
        self.v2_1.addLayout(self.h2_16)
        self.v2_1.addLayout(self.h2_17)
        self.v2_1.addLayout(self.h2_18)
        
        self.v2_1.setAlignment(QtCore.Qt.AlignTop)
        
        self.g_box2_1 = QtWidgets.QGroupBox('Einbürgerungen')
        self.g_box2_1.setLayout(self.v2_1)
        self.g_box2_1.setAlignment(QtCore.Qt.AlignTop)
        
        # middle right (3)
        self.lab_dateiname2 = QtWidgets.QLabel('Dateiname: ')
        self.lab_dateiname2.setFixedWidth(90)       
        self.qline_file2 = QtWidgets.QLineEdit()
        self.qline_file2.setReadOnly(True)
        self.qline_file2.setText(self.straftaten.get_filename())

        self.lab_deliktart = QtWidgets.QLabel('Deliktart')
        self.lab_deliktart.setFixedWidth(90)
        
        self.qlist_deliktart = QtWidgets.QListWidget()
        self.qlist_deliktart.setMinimumWidth(50)
        self.qlist_deliktart.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.qlist_deliktart.addItems(['(Alle)'] + self.straftaten.get_crime_cats_list())
        self.qlist_deliktart.setCurrentRow(0)
        self.qlist_deliktart.itemSelectionChanged.connect(self.create_df2)
        
        self.lab_durchschnitt2 = QtWidgets.QLabel('Durchschnitt')
        self.lab_durchschnitt2.setFixedWidth(90)
        self.lab_max2 = QtWidgets.QLabel('Maximum')
        self.lab_max2.setFixedWidth(90)
        self.lab_min2 = QtWidgets.QLabel('Minimum')
        self.lab_min2.setFixedWidth(90)
        self.lab_sa2 = QtWidgets.QLabel('S.abweichung')
        self.lab_sa2.setFixedWidth(90)
        
        self.qline_durchschnitt2 = QtWidgets.QLineEdit()
        self.qline_durchschnitt2.setAlignment(QtCore.Qt.AlignRight)
        self.qline_durchschnitt2.setReadOnly(True)
        self.qline_max2 = QtWidgets.QLineEdit()
        self.qline_max2.setAlignment(QtCore.Qt.AlignRight)
        self.qline_max2.setReadOnly(True)
        self.qline_min2 = QtWidgets.QLineEdit()
        self.qline_min2.setAlignment(QtCore.Qt.AlignRight)
        self.qline_min2.setReadOnly(True)
        self.qline_sa2 = QtWidgets.QLineEdit()
        self.qline_sa2.setAlignment(QtCore.Qt.AlignRight)
        self.qline_sa2.setReadOnly(True)

        self.but_graph2 = QtWidgets.QPushButton('Zeige Entwicklung')
        self.but_graph2.setFixedWidth(100)
        self.but_graph2.clicked.connect(self.but_graph2_clicked)

        self.h3_1 = QtWidgets.QHBoxLayout()
        self.h3_1.addWidget(self.lab_dateiname2)
        self.h3_1.addWidget(self.qline_file2)    
        self.h3_2 = QtWidgets.QHBoxLayout()
        self.h3_2.addWidget(self.lab_deliktart)
        self.h3_2.setAlignment(QtCore.Qt.AlignTop)    
        self.h3_3 = QtWidgets.QHBoxLayout()
        self.h3_3.addLayout(self.h3_2)
        self.h3_3.addWidget(self.qlist_deliktart)
        
        self.h3_4 = QtWidgets.QHBoxLayout()
        self.h3_4.addWidget(self.lab_durchschnitt2)
        self.h3_4.addWidget(self.qline_durchschnitt2)
        self.h3_4.setAlignment(QtCore.Qt.AlignTop)
        
        self.h3_5 = QtWidgets.QHBoxLayout()
        self.h3_5.addWidget(self.lab_max2)
        self.h3_5.addWidget(self.qline_max2)
        self.h3_5.setAlignment(QtCore.Qt.AlignTop)
        
        self.h3_6 = QtWidgets.QHBoxLayout()
        self.h3_6.addWidget(self.lab_min2)
        self.h3_6.addWidget(self.qline_min2)
        self.h3_6.setAlignment(QtCore.Qt.AlignTop)
        
        self.h3_7 = QtWidgets.QHBoxLayout()
        self.h3_7.addWidget(self.lab_sa2)
        self.h3_7.addWidget(self.qline_sa2)
        self.h3_7.setAlignment(QtCore.Qt.AlignTop)
        
        self.h3_8 = QtWidgets.QHBoxLayout()
        self.h3_8.addWidget(self.but_graph2)
        self.h3_8.setAlignment(QtCore.Qt.AlignRight)
                
        self.v3_1 = QtWidgets.QVBoxLayout()
        self.v3_1.addLayout(self.h3_1)
        self.v3_1.addLayout(self.h3_3)
        self.v3_1.addLayout(self.h3_4)
        self.v3_1.addLayout(self.h3_5)
        self.v3_1.addLayout(self.h3_6)
        self.v3_1.addLayout(self.h3_7)
        self.v3_1.addLayout(self.h3_8)
        self.v3_1.setAlignment(QtCore.Qt.AlignTop)
        
        self.g_box3_1 = QtWidgets.QGroupBox('Straftaten')
        self.g_box3_1.setLayout(self.v3_1)
        
        # middle (2) + (3)
        self.h_mid = QtWidgets.QHBoxLayout()
        self.h_mid.addWidget(self.g_box2_1)
        self.h_mid.addWidget(self.g_box3_1)
        self.h_mid.setAlignment(QtCore.Qt.AlignTop)
        
        # all (4)        
        self.v5_1 = QtWidgets.QVBoxLayout()
        self.v5_1.addWidget(self.g_box1_1)
        self.v5_1.addLayout(self.h_mid)
        self.v5_1.setAlignment(QtCore.Qt.AlignTop)
        
        self.setLayout(self.v5_1)
        
        self.create_df1()
        self.create_df2()
            
    def radio_but_land_toggled(self):
        if self.radio_but_land.isChecked():
            self.qlist_land.setEnabled(True)
            self.qlist_kontinent.setEnabled(False)
        else:
            self.qlist_land.setEnabled(False)
            self.qlist_kontinent.setEnabled(True)
        self.create_df1()
    
    def create_df1(self):
        df = self.einbuergerungen._df
        if len(self.qlist_jahre.selectedItems()) == 0:
            self.qlist_jahre.setCurrentRow(0)
        elif sorted([s.text() for s in self.qlist_jahre.selectedItems()])[0] == '(Alle)':
            pass
        elif sorted([s.text() for s in self.qlist_jahre.selectedItems()]) == self.einbuergerungen.get_years_list():
            pass
        else:
            df = df.loc[sorted([int(s.text()) for s in self.qlist_jahre.selectedItems()])]
        
        if self.qlist_land.isEnabled():
            if len(self.qlist_land.selectedItems()) == 0:
                self.qlist_land.setCurrentRow(0)
            elif sorted([s.text() for s in self.qlist_land.selectedItems()])[0] == '(Alle)':
                pass
            elif sorted([s.text() for s in self.qlist_land.selectedItems()]) == self.einbuergerungen.get_countries_list():
                pass
            else:
                df = df[df.iloc[:, 0].isin(sorted([s.text() for s in self.qlist_land.selectedItems()]))]
        else:
            if len(self.qlist_kontinent.selectedItems()) == 0:
                self.qlist_kontinent.setCurrentRow(0)
            elif sorted([s.text() for s in self.qlist_kontinent.selectedItems()])[0] == '(Alle)':
                pass
            elif sorted([s.text() for s in self.qlist_kontinent.selectedItems()]) == self.einbuergerungen.get_continents_list():
                pass
            else:
                df = df[df.iloc[:, 1].isin(sorted([s.text() for s in self.qlist_kontinent.selectedItems()]))]
        
        if len(self.qlist_geschlecht.selectedItems()) == 0:
            self.qlist_geschlecht.setCurrentRow(0)
        elif sorted([s.text() for s in self.qlist_geschlecht.selectedItems()])[0] == '(Alle)':
            pass
        elif sorted([s.text() for s in self.qlist_geschlecht.selectedItems()]) == self.einbuergerungen.get_sexes_list():
            pass
        else:
            df = df[df.iloc[:, 2].isin(sorted([s.text() for s in self.qlist_geschlecht.selectedItems()]))]
        
        if len(self.qlist_altersklasse.selectedItems()) == 0:
            self.qlist_altersklasse.setCurrentRow(0)
        elif sorted([s.text() for s in self.qlist_altersklasse.selectedItems()])[0] == '(Alle)':
            pass
        elif sorted([s.text() for s in self.qlist_altersklasse.selectedItems()]) == self.einbuergerungen.get_age_classes_list():
            pass
        elif self.qlist_altersklasse.selectedItems() == []:
            pass
        else:
            df = df[df.iloc[:, 3].isin(sorted([s.text() for s in self.qlist_altersklasse.selectedItems()]))]
        
        if not df.empty:                
            df = df.drop(df.columns[0:4], axis = 1)
            df = df.assign(j = '', z = '')
            list_unique_years = sorted(pd.unique(df.index.values).tolist())
            for u in range(len(list_unique_years)):
                df.iloc[u, 1] = list_unique_years[u]
                df.iloc[u, 2] = df.ix[list_unique_years[u], 0].sum()
            df = df.drop(df.columns[0], axis = 1)
            df = df.loc[df['j'] != '']
            df = df.set_index('j')
            df = df.reindex([y for y in range(min(list(df.index.values)), max(list(df.index.values)) + 1)], fill_value = 0)
            self.df1 = df
            self.df_status[0] = True
        else:
            self.df1 = None
            self.df_status[0] = False
        self.update_einbuergerungen()
        
    def update_einbuergerungen(self):
        if self.df_status[0]:
            self.qline_durchschnitt1.setText(str(float(self.df1.mean())))
            self.qline_max1.setText(str(float(self.df1.max())))
            self.qline_min1.setText(str(float(self.df1.min())))
            self.qline_sa1.setText(str(float(self.df1.std())))
        else:
            self.qline_durchschnitt1.setText('nan')
            self.qline_max1.setText('nan')
            self.qline_min1.setText('nan')
            self.qline_sa1.setText('nan')
        
    def but_graph1_clicked(self):
        if self.df_status[0] and len(self.df1.index) != 1:
            ax = plt.figure().gca()
            ax.xaxis.set_major_locator(MaxNLocator(integer = True))
            ax.yaxis.set_major_locator(MaxNLocator(integer = True))
            ax.get_xaxis().get_major_formatter().set_useOffset(False)
            plt.xlabel('Zeit', fontsize = 10)
            plt.ylabel('Anzahl Einbürgerungen', fontsize = 10)
            plt.suptitle('Einbürgerungen', fontsize = 20)
            plt.plot(self.df1, marker = '.')
            plt.show()
    
    def create_df2(self):
        df = self.straftaten._df
        if sorted([s.text() for s in self.qlist_jahre.selectedItems()])[0] == '(Alle)':
            pass
        elif sorted([s.text() for s in self.qlist_jahre.selectedItems()]) == self.straftaten.get_years_list():
            pass
        else:
            df = df.loc[sorted([int(s.text()) for s in self.qlist_jahre.selectedItems()])]
        
        if len(self.qlist_deliktart.selectedItems()) == 0:
            self.qlist_deliktart.setCurrentRow(0)
        elif sorted([s.text() for s in self.qlist_deliktart.selectedItems()])[0] == '(Alle)':
            pass
        elif sorted([s.text() for s in self.qlist_deliktart.selectedItems()]) == self.straftaten.get_crime_cats_list():
            pass
        elif self.qlist_deliktart.selectedItems() == []:
            pass
        else:
            df = df[[s.text() for s in self.qlist_deliktart.selectedItems()]]
        
        if not df.empty:
            df = df.assign(t = df.sum(axis = 1))
            df = df.drop(df.columns[:-1], axis = 1)
            self.df2 = df
            self.df_status[1] = True
        else:
            self.df2 = None
            self.df_status[1] = False
        self.update_straftaten()
        
    def update_straftaten(self):
        if self.df_status[1]:
            self.qline_durchschnitt2.setText(str(float(self.df2.mean())))
            self.qline_max2.setText(str(float(self.df2.max())))
            self.qline_min2.setText(str(float(self.df2.min())))
            self.qline_sa2.setText(str(float(self.df2.std())))
        else:
            self.qline_durchschnitt2.setText('nan')
            self.qline_max2.setText('nan')
            self.qline_min2.setText('nan')
            self.qline_sa2.setText('nan')
            
    def but_graph2_clicked(self):
        if self.df_status[1] and len(self.df2.index) != 1:
            ax = plt.figure().gca()
            ax.xaxis.set_major_locator(MaxNLocator(integer = True))
            ax.yaxis.set_major_locator(MaxNLocator(integer = True))
            ax.get_xaxis().get_major_formatter().set_useOffset(False)
            plt.xlabel('Zeit', fontsize = 10)
            plt.ylabel('Anzahl Straftaten', fontsize = 10)
            plt.suptitle('Straftaten', fontsize = 20)
            plt.plot(self.df2, '-r.')
            plt.show()

app = QtWidgets.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())      