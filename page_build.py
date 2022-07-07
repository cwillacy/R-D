# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 13:29:37 2021

@author: Christopher.Willacy
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPlainTextEdit, QProgressBar

#----------------------------------------------------------------------
#   OUTPUT OPTIONS
#----------------------------------------------------------------------
def PageBuild(self,Wizard,icons,df,tipstyle,groupstyle,labelstyle,library,project): 
    
    self.wizardPage9 = QtWidgets.QWizardPage()
    self.wizardPage9.setObjectName("wizardPage9")
    self.wizardPage9.setTitle("Build Status")
    self.verticalLayout_7b = QtWidgets.QVBoxLayout(self.wizardPage9)
    self.verticalLayout_7b.setObjectName("verticalLayout_7b")

    #----------------------------------------------------------------------------    
    self.groupBox_builds = QtWidgets.QGroupBox(self.wizardPage9)
    font = QtGui.QFont()
    font.setPointSize(12)
    self.groupBox_builds.setFont(font)
    self.groupBox_builds.setStyleSheet(groupstyle)
    self.groupBox_builds.setObjectName("groupBox_builds")
    self.groupBox_builds.setTitle("Progress")
    self.verticalLayout_7b.addWidget(self.groupBox_builds)
       
    self.verticalLayout_prog = QtWidgets.QVBoxLayout(self.groupBox_builds)
    self.verticalLayout_prog.setObjectName("verticalLayout_prog")
    self.horizontalLayout_prog = QtWidgets.QHBoxLayout()
    self.horizontalLayout_prog.setObjectName("horizontalLayout_prog")
     
    self.pushButton_build = QtWidgets.QPushButton(self.groupBox_builds)
    self.pushButton_build.setObjectName("pushButton_build")
    self.pushButton_build.setStyleSheet("border: none \
                                        min-width: 100px \
                                        min-height: 100px")

    
    self.pushButton_build.setDisabled(False)

    self.pushButton_build.setIcon(QIcon(icons[4])) 
    self.pushButton_build.clicked.connect(self.bld)
    self.horizontalLayout_prog.addWidget(self.pushButton_build)
    
    # creating progress bar
    self.bar = QProgressBar(self.groupBox_builds)
    self.bar.setGeometry(200, 150, 200, 30)
    self.bar.setMaximum(100)
    self.bar.setValue(0)

    self.horizontalLayout_prog.addWidget(self.bar)   
    self.verticalLayout_prog.addLayout(self.horizontalLayout_prog) 
 
    
    #---------------------------------------------------------------------------
    self.groupBox_log = QtWidgets.QGroupBox(self.wizardPage9)
    font = QtGui.QFont()
    font.setPointSize(12)
    self.groupBox_log.setFont(font)
    self.groupBox_log.setStyleSheet(groupstyle)
    self.groupBox_log.setObjectName("groupBox_log")
    self.groupBox_log.setTitle("Build Log")
    
    self.verticalLayout_log = QtWidgets.QVBoxLayout(self.groupBox_log)
    self.verticalLayout_log.setObjectName("verticalLayout_log")
    self.horizontalLayout_log = QtWidgets.QHBoxLayout()
    self.horizontalLayout_log.setObjectName("horizontalLayout_log")
        
    self.textBox_log = QPlainTextEdit(self.wizardPage9)  
    self.textBox_log.setReadOnly(True)

    self.textBox_log.ensureCursorVisible()
    self.textBox_log.setCenterOnScroll(True)
        
    self.horizontalLayout_log.addWidget(self.textBox_log)
    self.verticalLayout_log.addLayout(self.horizontalLayout_log)
  
    self.verticalLayout_7b.addWidget(self.groupBox_log)
     
    Wizard.setPage(9,self.wizardPage9)