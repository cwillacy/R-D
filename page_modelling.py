# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 13:18:52 2021

@author: Christopher.Willacy
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon

#----------------------------------------------------------------------
#  GEOMETRY PAGE
#----------------------------------------------------------------------
def PageModel(self,Wizard,icons,tipstyle,groupstyle,labelstyle):  
    self.wizardPage_mod = QtWidgets.QWizardPage()
    self.wizardPage_mod.setObjectName("wizardPage_mod")
    self.wizardPage_mod.setTitle("Trace Data Selection")
    self.verticalLayout_modpage = QtWidgets.QGridLayout(self.wizardPage_mod)
    self.verticalLayout_modpage.setObjectName("verticalLayout_modpage")   
    
    self.groupBox_mod = QtWidgets.QGroupBox(self.wizardPage_mod)
    font = QtGui.QFont()
    font.setPointSize(12)
    self.groupBox_mod.setFont(font)
    self.groupBox_mod.setStyleSheet(groupstyle)
    self.groupBox_mod.setObjectName("groupBox_mod")
    self.groupBox_mod.setTitle('Trace Data')
    self.verticalLayout_mod = QtWidgets.QVBoxLayout(self.groupBox_mod)
    self.verticalLayout_mod.setObjectName("verticalLayout_mod")    
    self.horizontalLayout_mod = QtWidgets.QHBoxLayout()
    self.horizontalLayout_mod.setObjectName("horizontalLayout_mod")
     
    self.label_mod = QtWidgets.QLabel(self.groupBox_mod)
    self.label_mod.setBaseSize(QtCore.QSize(0, 0))
    self.label_mod.setObjectName("label_mod")
    self.label_mod.setStyleSheet(labelstyle)
    self.label_mod.setText("Jobpro Dataset:")
    self.horizontalLayout_mod.addWidget(self.label_mod)
   
    self.lineEdit_mod= QtWidgets.QLineEdit(self.groupBox_mod)
    self.lineEdit_mod.setObjectName("lineEdit_mod")   
    self.lineEdit_mod.setToolTip("existing modelled or field traces can be assigned here using a Jobpro dataset name")
    self.lineEdit_mod.setStyleSheet(tipstyle)
    self.lineEdit_mod.setDisabled(False) 
    self.lineEdit_mod.textChanged[str].connect(self.changestate_mod)
    self.horizontalLayout_mod.addWidget(self.lineEdit_mod)    
    
    self.pushButton_data = QtWidgets.QPushButton(self.groupBox_mod)
    self.pushButton_data.setObjectName("pushButton_data")
    self.pushButton_data.setStyleSheet("border: none")
    self.pushButton_data.setIcon(QIcon(icons[3])) 
    self.pushButton_data.setDisabled(False)        
    self.pushButton_data.clicked.connect(self.openFileNameDialog_data)
    self.horizontalLayout_mod.addWidget(self.pushButton_data)
    
    self.verticalLayout_mod.addLayout(self.horizontalLayout_mod)  

    self.horizontalLayout_modins = QtWidgets.QHBoxLayout()
    self.horizontalLayout_modins.setObjectName("horizontalLayout_ins")
    self.label_modins = QtWidgets.QLabel(self.groupBox_mod)
    self.label_modins.setBaseSize(QtCore.QSize(0, 0))
    self.label_modins.setObjectName("label_mod")
    self.label_modins.setStyleSheet(labelstyle)

    mystring = '''\n\nOPTION 1: If modelled or field traces are already available, then they can be included here by providing the Jobpro dataset \
name in the text box above.\n\nOPTION 2: If the user would like to create synthetic traces for the acqusition design, then this can be achieved using \
the existing Jobpro modelling wizards (e.g. FWI, RTMIG, WFD). In this instance, no entry is needed in the text box above and the user will be required \
to manually enter the dataset name in the post-modelling skeleton (e.g., 04_pos_mod_comb.skl).'''

    self.label_modins.setText(mystring)
    self.label_modins.setWordWrap(True)

    notificationstyle = str("QLabel {\n"
                 "  color: blue;\n"
                 "  font-size: 16px;\n"
                 "}")   
    self.label_modins.setStyleSheet(notificationstyle)
    self.horizontalLayout_modins.addWidget(self.label_modins)
    self.verticalLayout_mod.addLayout(self.horizontalLayout_modins) 
    self.verticalLayout_modpage.addWidget(self.groupBox_mod) 
    
    Wizard.setPage(5,self.wizardPage_mod)        