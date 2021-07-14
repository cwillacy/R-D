# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 11:57:47 2021

@author: Christopher.Willacy
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPlainTextEdit

#----------------------------------------------------------------------
#  INTRO PAGE
#----------------------------------------------------------------------
def PageIntro(self,Wizard,icons,tipstyle,groupstyle):

    self.wizardPage1 = QtWidgets.QWizardPage()
    self.wizardPage1.setTitle("Introduction")
    self.wizardPage1.setObjectName("wizardPage1")        
    self.verticalLayout_2in = QtWidgets.QVBoxLayout(self.wizardPage1)
    self.verticalLayout_2in.setObjectName("verticalLayout_2in")
    self.groupBox_3in = QtWidgets.QGroupBox(self.wizardPage1)
    font = QtGui.QFont()
    font.setPointSize(12)
    self.groupBox_3in.setFont(font)
    self.groupBox_3in.setStyleSheet(groupstyle)
    self.groupBox_3in.setObjectName("groupBox_3in")
    self.groupBox_3in.setTitle("")
    self.verticalLayout_3in = QtWidgets.QVBoxLayout(self.groupBox_3in)
    self.verticalLayout_3in.setObjectName("verticalLayout_3in")
    self.horizontalLayout_9in = QtWidgets.QHBoxLayout()
    self.horizontalLayout_9in.setObjectName("horizontalLayout_9in")
    self.label = QtWidgets.QLabel(self.groupBox_3in)
    self.label.setBaseSize(QtCore.QSize(0, 0))
    self.label.setObjectName("label")
    self.label.setWordWrap(True)
    self.label.setText("<html><head/><body><p><span style=\" font-size:12pt; color:#0000ff;\">Welcome to SimWiz</span></<br/></p><p><span style=\" color:#000000;\">The wizard builds \
                           skeletons that provide the following functions:</span></p><p>- Convert SPS to SAF format</p><p>- Create a merged acquisition \
                               geometry</p><p>- Generate ssf traces for modelling</p><p>- Updating of trace idents post modelling</p><p>- Blending the \
                                   data</p><p>- Deblending the \
                                   data</p><p>- Data QC</p></body></html>")
                                   
    self.label.setAlignment(Qt.AlignTop)
    self.horizontalLayout_9in.addWidget(self.label)            
    self.label_r = QtWidgets.QLabel(self.groupBox_3in)
    self.label_r.setBaseSize(QtCore.QSize(0, 0))
    self.label_r.setObjectName("label")        
    self.label_r.setPixmap(QtGui.QPixmap('img/side-bar2.png'))
    self.label_r.setAlignment(Qt.AlignTop)
    self.horizontalLayout_9in.addWidget(self.label_r)         
    self.verticalLayout_3in.addLayout(self.horizontalLayout_9in)        
    self.verticalLayout_2in.addWidget(self.groupBox_3in) 
       
    self.groupBox_4in = QtWidgets.QGroupBox(self.wizardPage1)
    font = QtGui.QFont()
    font.setPointSize(12)
    self.groupBox_4in.setFont(font)
    self.groupBox_4in.setStyleSheet(groupstyle)
    self.groupBox_4in.setObjectName("groupBox_4in")
    self.groupBox_4in.setTitle("Open Previous Wizard Setup")
    self.verticalLayout_4in = QtWidgets.QVBoxLayout(self.groupBox_4in)
    self.verticalLayout_4in.setObjectName("verticalLayout_4in")
    self.horizontalLayout_12in = QtWidgets.QHBoxLayout()
    self.horizontalLayout_12in.setObjectName("horizontalLayout_12in")
    self.verticalLayout_2in.addWidget(self.groupBox_4in)       
    self.label_in = QtWidgets.QLabel(self.groupBox_4in)
    self.label_in.setBaseSize(QtCore.QSize(0, 0))
    self.label_in.setObjectName("label_in")
    self.label_in.setText("Load Parameters:")  
    self.label_in.setFixedWidth(135)              
    self.horizontalLayout_12in.addWidget(self.label_in)       
    self.lineEdit_5in = QtWidgets.QLineEdit(self.groupBox_4in)
    self.lineEdit_5in.setObjectName("lineEdit_5in")
    self.lineEdit_5in.setText('')
    self.horizontalLayout_12in.addWidget(self.lineEdit_5in)       
    self.lineEdit_5in.setToolTip("enter a previous SimWiz configuration file")
    self.lineEdit_5in.setStyleSheet(tipstyle)    
    self.pushButton_3in = QtWidgets.QPushButton(self.groupBox_4in)
    self.pushButton_3in.setObjectName("pushButton_3in")
    self.pushButton_3in.setStyleSheet("border: none")
    self.pushButton_3in.setIcon(QIcon(icons[3])) 
    
    self.horizontalLayout_12in.addWidget(self.pushButton_3in)
    self.verticalLayout_4in.addLayout(self.horizontalLayout_12in) 

    self.horizontalLayout_desc = QtWidgets.QHBoxLayout()
    self.horizontalLayout_desc.setObjectName("horizontalLayout_desc")
      
    self.label_desc = QtWidgets.QLabel(self.groupBox_4in)
    self.label_desc.setBaseSize(QtCore.QSize(0, 0))
    self.label_desc.setObjectName("label_desc")
    self.label_desc.setText("Description:")  
    self.label_desc.setFixedWidth(135)              
    self.horizontalLayout_desc.addWidget(self.label_desc) 

    self.textBox = QPlainTextEdit(self.wizardPage1)   
    
    self.horizontalLayout_desc.addWidget(self.textBox)
    self.textBox.textChanged.connect(self.changestate_desc)
    
    self.pushButton_desc = QtWidgets.QPushButton(self.groupBox_4in)
    self.pushButton_desc.setObjectName("pushButton_desc")
    self.pushButton_desc.setStyleSheet("border: none")
    self.pushButton_desc.setIcon(QIcon(icons[2])) 
    self.horizontalLayout_desc.addWidget(self.pushButton_desc)
    
    self.verticalLayout_4in.addLayout(self.horizontalLayout_desc) 
    #----------------

    Wizard.setPage(1,self.wizardPage1)
   
    self.pushButton_3in.clicked.connect(self.openFileNameDialog_in) 
    
