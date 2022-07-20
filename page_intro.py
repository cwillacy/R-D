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
def PageIntro(self,Wizard,icons,tipstyle,groupstyle,labelstyle,lineeditstyle):

    self.wizardPage1 = QtWidgets.QWizardPage()
    self.wizardPage1.setTitle("Introduction")
    self.wizardPage1.setObjectName("wizardPage1")        
    self.verticalLayout_2in = QtWidgets.QVBoxLayout(self.wizardPage1)
    self.verticalLayout_2in.setObjectName("verticalLayout_2in")
    self.groupBox_3in = QtWidgets.QGroupBox(self.wizardPage1)
    font = QtGui.QFont()
    font.setPointSize(12)
    
    welcomestyle = str("QLabel {\n"
                 "  color: blue;\n"
                 "  font-size: 18px;\n"
                 "}")   
    
    funcstyle = str("QLabel {\n"
                 "  color: black;\n"
                 "  font-size: 14px;\n"
                 "}")  
        
    self.groupBox_3in.setFont(font)
    self.groupBox_3in.setStyleSheet(groupstyle)
    self.groupBox_3in.setObjectName("groupBox_3in")
    self.groupBox_3in.setTitle("")
    self.verticalLayout_3in = QtWidgets.QVBoxLayout(self.groupBox_3in)
    self.verticalLayout_3in.setObjectName("verticalLayout_3in")
    self.horizontalLayout_9in = QtWidgets.QHBoxLayout()
    self.horizontalLayout_9in.setObjectName("horizontalLayout_9in")
    
    self.verticalLayout_lside = QtWidgets.QVBoxLayout()
    self.verticalLayout_lside.setObjectName("verticalLayout_lside")
    self.verticalLayout_rside = QtWidgets.QVBoxLayout()
    self.verticalLayout_rside.setObjectName("verticalLayout_rside")

    self.label = QtWidgets.QLabel(self.groupBox_3in)
    self.label.setObjectName("label")
    self.label.setStyleSheet(welcomestyle)
    self.label.setWordWrap(True)                                                                   
    self.label.setText("Welcome to SimWiz")
    
    # self.label.setText("<html><head/><body><p><span style=\" font-size:12pt; color:#0000ff;\">Welcome to SimWiz</span></<br/></p><p><span style=\" color:#000000;\">This wizard performs \
    #                        the following functions:</span></p><p>- Generates deblending skeletons \
    #                                </p><p>- Provides segment optimization</p></p><p>- Provides data QC</body></html>")
    
    #self.label.setFixedWidth(155)               
    self.label.setAlignment(Qt.AlignTop)
    self.verticalLayout_lside.addWidget(self.label)  
    
    self.label_func = QtWidgets.QLabel(self.groupBox_3in)
    self.label_func.setObjectName("label_func")
    self.label_func.setStyleSheet(funcstyle)
    self.label_func.setText("Wizard functions:\n- SPS to SAF conversion\n- Build geometry\n- Generate SSF traces\n- Ident updating\n- Blending\n- Deblending")
    self.label_func.setAlignment(Qt.AlignVCenter)  
    self.label_func.setWordWrap(True)      
    self.verticalLayout_lside.addWidget(self.label_func)   
         
    self.label_r = QtWidgets.QLabel(self.groupBox_3in)
    self.label_r.setBaseSize(QtCore.QSize(0, 0))
    self.label_r.setObjectName("label_r")       
    self.label_r.setPixmap(QtGui.QPixmap('img/side-bar4.png'))
    self.label_r.setAlignment(Qt.AlignTop)
    
    self.verticalLayout_rside.addWidget(self.label_r)     
    self.horizontalLayout_9in.addLayout(self.verticalLayout_lside)  
    self.horizontalLayout_9in.addLayout(self.verticalLayout_rside)        

    self.verticalLayout_3in.addLayout(self.horizontalLayout_9in)        
    self.verticalLayout_2in.addWidget(self.groupBox_3in) 
   
    #------------------
    
    self.groupBox_4in = QtWidgets.QGroupBox(self.wizardPage1)
    font = QtGui.QFont()
    font.setPointSize(12)
    self.groupBox_4in.setFont(font)
    self.groupBox_4in.setStyleSheet(groupstyle)
    self.groupBox_4in.setObjectName("groupBox_4in")
    self.groupBox_4in.setTitle("Open Wizard Configuration File")
    self.verticalLayout_4in = QtWidgets.QVBoxLayout(self.groupBox_4in)
    self.verticalLayout_4in.setObjectName("verticalLayout_4in")
    self.horizontalLayout_12in = QtWidgets.QHBoxLayout()
    self.horizontalLayout_12in.setObjectName("horizontalLayout_12in")
    self.verticalLayout_2in.addWidget(self.groupBox_4in)       
    self.label_in = QtWidgets.QLabel(self.groupBox_4in)
    self.label_in.setBaseSize(QtCore.QSize(0, 0))
    self.label_in.setObjectName("label_in")
    self.label_in.setStyleSheet(labelstyle)
    self.label_in.setText("Load Parameters:")  
    self.label_in.setFixedWidth(155)              
    self.horizontalLayout_12in.addWidget(self.label_in)       
    self.lineEdit_5in = QtWidgets.QLineEdit(self.groupBox_4in)
    self.lineEdit_5in.setObjectName("lineEdit_5in")
    #self.lineEdit_5in.setStyleSheet(lineeditstyle)
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
    self.label_desc.setStyleSheet(labelstyle)
    self.label_desc.setText("Description:")  
    self.label_desc.setFixedWidth(155)              
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
    
