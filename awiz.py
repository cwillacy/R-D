# -*- coding: utf-8 -*-
#
# Application Wizard for building the sim source acquisition design skeletons
#
#
# Author: C. Willacy, 2021
#
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QIcon
import pandas as pd
import os
import build
import helpgui
import sidebar
import page_intro
import page_setup
import page_import
import page_geom
import page_noise
import page_blend
import page_deblend
import page_output

#------------------------------------------------------------------------------
#
#  Main GUI Class definition
#
#------------------------------------------------------------------------------
class Ui_Wizard(object):

    def setupUi(self, Wizard):
        global df, debug, Dialog, icons, tipstyle, groupstyle, storage
        
        # switch on debug mode
        debug=False
        
        icons = ['img/tools-wizard_32x32.png', 'img/arrowr-black.png', 'img/blank.png', 'img/document-open-folder.png']
        
        Wizard.setObjectName("Wizard")
        Wizard.setFixedSize(850, 525)
        Wizard.setAutoFillBackground(False) # switch off window resizing
        Wizard.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        Wizard.setWizardStyle(QtWidgets.QWizard.MacStyle)
        Wizard.setWindowTitle("SimWiz - Simultaneous Source Acquisition Design Wizard")
        #Wizard.setWindowIcon(QtGui.QIcon('img/draw-bezier-curves_32x32.png'))
        #Wizard.setWindowIcon(QtGui.QIcon("img/nepomuk_32x32.png"))
        Wizard.setWindowIcon(QtGui.QIcon(icons[0]))
                             
        #-----------build the side bar workflow selector--------------   
        sidebar.sideBar(self,icons,Wizard)  

        #-------style selection---------
        #Wizard.setWizardStyle(QtWidgets.QWizard.ClassicStyle)
        #Wizard.setWizardStyle(QtWidgets.QWizard.ModernStyle)
        #Wizard.setWizardStyle(QtWidgets.QWizard.AeroStyle)
               
        Wizard.setOptions(QtWidgets.QWizard.CancelButtonOnLeft|QtWidgets.QWizard.HaveHelpButton|QtWidgets.QWizard.NoDefaultButton)
        
        # nxt = Wizard.button(QtWidgets.QWizard.NextButton)
        # nxt.clicked.connect(self.providehelp)
        
        myhelp = Wizard.button(QtWidgets.QWizard.HelpButton)
                
        Dialog = None
        
        myhelp.clicked.connect(self.providehelp)       
        
        nxt = Wizard.button(QtWidgets.QWizard.NextButton)
        nxt.clicked.connect(self.nxtpage)
              
        bck = Wizard.button(QtWidgets.QWizard.BackButton)
        bck.clicked.connect(self.bckpage)
        
        done = Wizard.button(QtWidgets.QWizard.FinishButton)
        done.clicked.connect(self.done)
  
        tipstyle = str("""QToolTip { 
                       background-color: black; 
                       color: white; 
                       border: black solid 1px
                       }""")      
   
        groupstyle = str("QGroupBox {\n"
                         "  color: maroon;\n"
                         "  font-size: 12px;\n"
                         "}")   
                
        
        data = {'PARAMETER': ['ATYPE','SRCTYPE','SHTCOD','JOBREV','SPSSRC','SPSREC','SPSREL',
                                       'BSHIFT','X0','Y0','MIRR','MIRRZ','RECIP','INTERP','HORSAF',
                                       'NOISE','NOISEAPP','NOISEMODE','FACLEV','FLOW','IORLOW','FHIGH',
                                       'IORHIG','TMAX','DT','TOUT','T0','OUTDIR','SSF','QCGEOM','QCTIME',
                                       'QCDEPTH','SQSORT','SRTALL','CONV','WAVELET','POOL','DBL','FMAX',
                                       'NDIP','PMAX','MXBLND','XYWINDOW','TWINDOW','NITERS','NSHOT',
                                       'NWAVIT'],
                'VALUE': ['OBN','Single',0,000.00,'','','','False',0,0,'False',0,'True','False',
                          '','False','PRE','NDB',0,0,0,0,0,0,4,0,0,'','True','False','False','False',100,
                          4000,'False','','ird_ict1','False',20,30,'0.0008333',40,700,400,3,550,3]
                }
        
        df = pd.DataFrame(data, columns=['PARAMETER','VALUE'])


        storage = ["ird_ict1","sgsjpdata1","sgsjpdata2","sgsjpdata3","copydata","eptnmx","eptnobackup","eptram11scr_dyna", \
               "eptram11scratch","eptram12scratch","eptram13scratch","eptram14scratch","eptram15scratch","eptram16scratch", \
                   "eptram17scratch","eptram19scratch","eptram4scratch","eptram6scratch","eptram8scratch","epw0034_a5_3590h", \
                       "epw0034_a5_3592b3","epw_scr_3592b3","epw_tc_v3590h","epwjpdata1","epwreg5scratch","hou_hsm_ua",\
                           "hou_scr_gsp","hou_ua_usc_export","hou_vdisk_gsp","hou_vdisk_ua","hou_vt_ept","hou_vt_gsp",\
                               "hou_vt_train","hou_vt_ua","hougdc_vt_ept","ird_ict1_dyna","sasnobackup","sgs_trd_3590b",\
                                   "sgs_trd_3590e","sgs_trd_3590h","sgs_trd_3592a2","sgs_trd_3592a3","sgs_trd_3592b2",\
                                       "sgs_trd_3592b3","sgsgdc_tc_v3590h"]

        storage.sort()  

        if debug:
            print(df)

        #----------------------------------------------------------------------
        #  PAGE 1
        #----------------------------------------------------------------------
        page_intro.PageIntro(self,Wizard,icons,tipstyle,groupstyle)
        
        #----------------------------------------------------------------------
        #  PAGE 2
        #----------------------------------------------------------------------
        page_setup.PageSetup(self,Wizard,icons,tipstyle,groupstyle,storage)
                               
        #----------------------------------------------------------------------
        #  PAGE 3
        #----------------------------------------------------------------------
        page_import.PageImport(self,Wizard,icons,tipstyle,groupstyle)

        #----------------------------------------------------------------------
        #  PAGE 4
        #----------------------------------------------------------------------
        page_geom.PageGeom(self,Wizard,icons,tipstyle,groupstyle)
    
        #----------------------------------------------------------------------
        #  PAGE 5
        #----------------------------------------------------------------------
        page_noise.PageNoise(self,Wizard,icons,tipstyle,groupstyle)
                      
        #----------------------------------------------------------------------
        #  PAGE 6
        #----------------------------------------------------------------------
        page_blend.PageBlend(self,Wizard,icons,df,tipstyle,groupstyle)

        #----------------------------------------------------------------------
        #  PAGE 7
        #----------------------------------------------------------------------
        page_deblend.PageDeblend(self,Wizard,icons,df,tipstyle,groupstyle)
                
        #----------------------------------------------------------------------
        #  PAGE 8
        #----------------------------------------------------------------------
        page_output.PageOutput(self,Wizard,icons,df,tipstyle,groupstyle)
                       
        self.pushButton_2.clicked.connect(self.openFileNameDialog_out_dir)
        self.pushButton_3.clicked.connect(self.openFileNameDialog_sps_src)
        self.pushButton_4.clicked.connect(self.openFileNameDialog_sps_rec)
        self.pushButton_5.clicked.connect(self.openFileNameDialog_sps_rel)
        self.pushButton_6.clicked.connect(self.openFileNameDialog_hor_saf)
               
        QtCore.QMetaObject.connectSlotsByName(Wizard)


    #----------------------------------------------------------------------
    #  INTERFACE STATE UPDATE
    #----------------------------------------------------------------------            
    def updateInterface(self):
        global df, debug
        
        #---------------------ATYPE---------------------
        val = df.loc[0,"VALUE"]

        if val == "OBN":
            index=0
        elif val == "Streamer":
            index=1
        else:
            index=2
        
        self.comboBox.setCurrentIndex(index)                 
        #---------------------SRCTYPE---------------------
        val = df.loc[1,"VALUE"]

        if val == "Single":
            index=0
            self.lineEdit_shtcod.setDisabled(True)
        else:
            index=1
            self.lineEdit_shtcod.setDisabled(False)
            
       
        self.comboBox_2.setCurrentIndex(index)        
        #---------------------SHTCOD---------------------
        val = df.loc[2,"VALUE"]
        self.lineEdit_shtcod.setText(val)
        #---------------------JOBREV---------------------
        val = df.loc[3,"VALUE"]
        self.lineEdit.setText(val)
        #---------------------SPSSRC---------------------
        val = str(df.loc[4,"VALUE"])
        self.lineEdit_5.setText(val)
        #---------------------SPSREC---------------------
        val = str(df.loc[5,"VALUE"])
        self.lineEdit_6.setText(val)      
        #---------------------SPSREL---------------------
        val = str(df.loc[6,"VALUE"])
        self.lineEdit_7.setText(val)       
        #---------------------BSHIFT---------------------
        val = df.loc[7,"VALUE"]
        if val == 'True':
            self.checkBox_4.setChecked(True)  
            self.lineEdit_8.setDisabled(False)
            self.lineEdit_9.setDisabled(False)
        else:
            self.checkBox_4.setChecked(False) 
            self.lineEdit_8.setDisabled(True)
            self.lineEdit_9.setDisabled(True)     
        #---------------------X0---------------------  
        val = df.loc[8,"VALUE"]
        self.lineEdit_8.setText(val)        
        #---------------------Y0---------------------  
        val = df.loc[9,"VALUE"]
        self.lineEdit_9.setText(val)  
        #---------------------MIRR---------------------
        val = df.loc[10,"VALUE"]
        if val == 'True':
            self.checkBox.setChecked(True)  
            self.lineEdit_3.setDisabled(False)
        else:
            self.checkBox.setChecked(False) 
            self.lineEdit_3.setDisabled(True)
        #---------------------MIRRZ---------------------
        val = df.loc[11,"VALUE"]
        self.lineEdit_3.setText(val)       
        #---------------------RECIP---------------------
        val = df.loc[12,"VALUE"]
        if val == 'True':
            self.checkBox_2.setChecked(True)  
        else:
            self.checkBox_2.setChecked(False)              
        #---------------------INTERP---------------------
        val = df.loc[13,"VALUE"]
        if val == 'True':
            self.checkBox_5.setChecked(True)  
            self.lineEdit_10.setDisabled(False)
            self.pushButton_6.setDisabled(False)
        else:
            self.checkBox_5.setChecked(False)   
            self.lineEdit_10.setDisabled(True)
            self.pushButton_6.setDisabled(True)
            
        val = str(df.loc[14,"VALUE"])
        self.lineEdit_10.setText(val)
        #---------------------NOISE---------------------        
        val = df.loc[15,"VALUE"]
        
        if val == 'True':
             self.checkBox_5b.setChecked(True) 
             self.comboBox_3b.setDisabled(False)
             self.radioButton_1.setDisabled(False)              
             self.radioButton_2.setDisabled(False) 
             self.lineEdit_faclev.setDisabled(False)
             self.lineEdit_flow.setDisabled(False)
             self.lineEdit_iorlow.setDisabled(False)
             self.lineEdit_fhigh.setDisabled(False)
             self.lineEdit_iorhig.setDisabled(False)
        else:
             self.checkBox_5b.setChecked(False) 
             self.comboBox_3b.setDisabled(True)
             self.radioButton_1.setDisabled(True) 
             self.radioButton_2.setDisabled(True) 
             self.lineEdit_faclev.setDisabled(True)
             self.lineEdit_flow.setDisabled(True)
             self.lineEdit_iorlow.setDisabled(True)
             self.lineEdit_fhigh.setDisabled(True)
             self.lineEdit_iorhig.setDisabled(True)
             
        val = df.loc[38,"VALUE"]    
        self.lineEdit_dbl2a.setText(val)
        val = df.loc[39,"VALUE"]    
        self.lineEdit_dbl2b.setText(val)        
        val = df.loc[40,"VALUE"]    
        self.lineEdit_dbl3a.setText(val)        
        val = df.loc[41,"VALUE"]    
        self.lineEdit_dbl3b.setText(val)        
        val = df.loc[42,"VALUE"]    
        self.lineEdit_dbl4a.setText(val)        
        val = df.loc[43,"VALUE"]    
        self.lineEdit_dbl4b.setText(val)        
        val = df.loc[44,"VALUE"]    
        self.lineEdit_dbl5a.setText(val)  
        val = df.loc[45,"VALUE"]    
        self.lineEdit_dbl5b.setText(val)  
        val = df.loc[46,"VALUE"]    
        self.lineEdit_dbl6a.setText(val)  
        
        val = df.loc[16,"VALUE"]
        if val == 'POS':
            self.radioButton_2.setChecked(True)  
        else:
            self.radioButton_1.setChecked(True) 
            
            
        val = df.loc[17,"VALUE"]

        if val == "SNR":
            index=1
        else:
            index=0
       
        self.comboBox_3b.setCurrentIndex(index) 
        val = df.loc[18,"VALUE"]
        self.lineEdit_faclev.setText(val)
        val = df.loc[19,"VALUE"]
        self.lineEdit_flow.setText(val)
        val = df.loc[20,"VALUE"]
        self.lineEdit_iorlow.setText(val)
        val = df.loc[21,"VALUE"]
        self.lineEdit_fhigh.setText(val)
        val = df.loc[22,"VALUE"]
        self.lineEdit_iorhig.setText(val)
        val = df.loc[23,"VALUE"]
        self.lineEdit_tmax.setText(val)
        val = df.loc[24,"VALUE"]
        self.lineEdit_dt.setText(val)
        val = df.loc[25,"VALUE"]
        self.lineEdit_tout.setText(val)
        val = df.loc[26,"VALUE"]
        self.lineEdit_t0.setText(val)
        val = df.loc[27,"VALUE"]
        self.lineEdit_4.setText(str(val))
        val = df.loc[28,"VALUE"]
        if val == 'True':
            self.checkBox_3.setChecked(True)
        else:
            self.checkBox_3.setChecked(False)
           
        val = df.loc[29,"VALUE"]
        if val == 'True':
            self.checkBox_6.setChecked(True)
        else:
            self.checkBox_6.setChecked(False)   
    
        val = df.loc[30,"VALUE"]
        if val == 'True':
            self.checkBox_7.setChecked(True)
        else:
            self.checkBox_7.setChecked(False)          
            
        val = df.loc[31,"VALUE"]
        if val == 'True':
            self.checkBox_8.setChecked(True)
        else:
            self.checkBox_8.setChecked(False) 
      
        val = df.loc[32,"VALUE"]
        self.lineEdit_sqsaf.setText(val)    
        val = df.loc[33,"VALUE"]
        self.lineEdit_srtall.setText(val)  
        #---------------------WAVELET---------------------
        val = df.loc[34,"VALUE"]
        if val == 'True':
            self.checkBox_wavelet.setChecked(True)  
            self.lineEdit_wavelet.setDisabled(False)
            self.pushButton_wavelet.setDisabled(False)
        else:
            self.checkBox_wavelet.setChecked(False) 
            self.lineEdit_wavelet.setDisabled(True)
            self.pushButton_wavelet.setDisabled(True)
             
        val = str(df.loc[35,"VALUE"])
        self.lineEdit_wavelet.setText(val) 
        
        #---------------------POOL---------------------
        val = df.loc[36,"VALUE"]

        index = storage.index(val)
       
        self.comboBox_pool.setCurrentIndex(index)  
        
        #---------------------DBL---------------------
        val = df.loc[37,"VALUE"]
        if val == 'True':
            self.checkBox_dbl.setChecked(True)  
            self.lineEdit_dbl2a.setDisabled(False)
            self.lineEdit_dbl2b.setDisabled(False)
            self.lineEdit_dbl3a.setDisabled(False)
            self.lineEdit_dbl3b.setDisabled(False)
            self.lineEdit_dbl4a.setDisabled(False)
            self.lineEdit_dbl4b.setDisabled(False)
            self.lineEdit_dbl5a.setDisabled(False)
            self.lineEdit_dbl5b.setDisabled(False)       
            self.lineEdit_dbl6a.setDisabled(False) 
        else:
            self.checkBox_dbl.setChecked(False) 
            self.lineEdit_dbl2a.setDisabled(True)
            self.lineEdit_dbl2b.setDisabled(True)
            self.lineEdit_dbl3a.setDisabled(True)
            self.lineEdit_dbl3b.setDisabled(True)
            self.lineEdit_dbl4a.setDisabled(True)
            self.lineEdit_dbl4b.setDisabled(True)
            self.lineEdit_dbl5a.setDisabled(True)
            self.lineEdit_dbl5b.setDisabled(True)   
            self.lineEdit_dbl6a.setDisabled(True)  
            
    #----------------------------------------------------------------------
    #  PARAMETER FILE DIALOG
    #----------------------------------------------------------------------
    def openFileNameDialog_in(self):
        global df, debug
        self.dialog_in = QFileDialog()
        self.dialog_in.setWindowTitle('Open SimWiz Parameter File')
        self.dialog_in.setFileMode(QFileDialog.AnyFile)
        self.dialog_in.setFilter(QDir.Files)
        self.dialog_in.setNameFilters(['SimWiz (*.csv)','All files (*.*)'])    
        self.dialog_in.setWindowIcon(QtGui.QIcon(icons[3]))
        self.dialog_in.setDirectory(r"user/")
        if self.dialog_in.exec_():
            file_name = self.dialog_in.selectedFiles()
            if debug:
                print(file_name)
        
            self.lineEdit_5in.setText(str(file_name[0]))
            #
            #  now read csv file and update pandas dataframe
            #       
            df = pd.read_csv(str(file_name[0]),keep_default_na=False)
              
            if debug:
                print(df)
                
            # make sure to update all interface widgets with the loaded parameters 
            self.updateInterface()                  
                          
    #----------------------------------------------------------------------
    #  SPS SRC DIALOG
    #----------------------------------------------------------------------        
    def openFileNameDialog_sps_src(self):
        global df, debug
        self.dialog = QFileDialog()
        self.dialog.setWindowTitle('Open SPS source file')
        self.dialog.setFileMode(QFileDialog.AnyFile)
        self.dialog.setFilter(QDir.Files)
        if self.dialog.exec_():
            file_name = self.dialog.selectedFiles()
            if debug:
                print(file_name)
            self.lineEdit_5.setText(str(file_name[0]))
            df.loc[df['PARAMETER'] == 'SPSSRC', 'VALUE'] = str(file_name[0])

    #----------------------------------------------------------------------
    #  SPS REC DIALOG
    #----------------------------------------------------------------------  
    def openFileNameDialog_sps_rec(self):
        global df, debug
        self.dialog = QFileDialog()
        self.dialog.setWindowTitle('Open SPS receiver file')
        self.dialog.setFileMode(QFileDialog.AnyFile)
        self.dialog.setFilter(QDir.Files)
        if self.dialog.exec_():
            file_name = self.dialog.selectedFiles()
            if debug:
                print(file_name)
            self.lineEdit_6.setText(str(file_name[0]))
            df.loc[df['PARAMETER'] == 'SPSREC', 'VALUE'] = str(file_name[0])

    #----------------------------------------------------------------------
    #  SPS RELATIONAL DIALOG
    #----------------------------------------------------------------------            
    def openFileNameDialog_sps_rel(self):
        global df, debug
        self.dialog = QFileDialog()
        self.dialog.setWindowTitle('Open SPS relational file')
        self.dialog.setFileMode(QFileDialog.AnyFile)
        self.dialog.setFilter(QDir.Files)
        if self.dialog.exec_():
            file_name = self.dialog.selectedFiles()
            if debug:
                print(file_name)
            self.lineEdit_7.setText(str(file_name[0]))
            df.loc[df['PARAMETER'] == 'SPSREL', 'VALUE'] = str(file_name[0])

    #----------------------------------------------------------------------
    #  WAVELET FILE DIALOG
    #---------------------------------------------------------------------- 
    def openFileNameDialog_wavelet(self):
        global df, debug
        self.dialog = QFileDialog()
        self.dialog.setWindowTitle('Select a WAVSAM file')
        self.dialog.setFileMode(QFileDialog.AnyFile)
        self.dialog.setFilter(QDir.Files)
        if self.dialog.exec_():
            file_name = self.dialog.selectedFiles()
            if debug:
                print(file_name)
            self.lineEdit_wavelet.setText(str(file_name[0]))
            df.loc[df['PARAMETER'] == 'WAVELET', 'VALUE'] = str(file_name[0])

    #----------------------------------------------------------------------
    #  TW HORIZON SAF FILE DIALOG
    #----------------------------------------------------------------------            
    def openFileNameDialog_hor_saf(self):
        global df, debug
        self.dialog = QFileDialog()
        self.dialog.setWindowTitle('Open SAF file')
        self.dialog.setFileMode(QFileDialog.AnyFile)
        self.dialog.setFilter(QDir.Files)
        if self.dialog.exec_():
            file_name = self.dialog.selectedFiles()
            if debug:
                print(file_name)
            self.lineEdit_10.setText(str(file_name[0]))
            df.loc[df['PARAMETER'] == 'HORSAF', 'VALUE'] = str(file_name[0])

    #----------------------------------------------------------------------
    #  OUTPUT SKL DIR
    #---------------------------------------------------------------------- 
    def openFileNameDialog_out_dir(self):
        global df, debug
        self.dialog = QFileDialog()
        self.dialog.setWindowTitle('Select output directory')
        self.dialog.setFileMode(QFileDialog.DirectoryOnly)
        self.dialog.setFilter(QDir.Files)
        if self.dialog.exec_():
            file_name = self.dialog.selectedFiles()
            self.lineEdit_4.setText(str(file_name[0]))
            df.loc[df['PARAMETER'] == 'OUTDIR', 'VALUE'] = str(file_name[0])
            
        if debug:
            print(df)
                       
    def changestate_bshift(self):
        global df, debug
        
        if (self.checkBox_4.isChecked()):
            self.lineEdit_8.setDisabled(False)
            self.lineEdit_9.setDisabled(False)
            df.loc[df['PARAMETER'] == 'BSHIFT', 'VALUE'] = 'True'
        else:
            self.lineEdit_8.setDisabled(True) 
            self.lineEdit_9.setDisabled(True)
            df.loc[df['PARAMETER'] == 'BSHIFT', 'VALUE'] = 'False'

        if debug:
            print(df)
            

    def changestate_mirr(self):
        global debug
        
        if (self.checkBox.isChecked()):
            self.lineEdit_3.setDisabled(False)
            df.loc[df['PARAMETER'] == 'MIRR', 'VALUE'] = 'True'
        else:
            self.lineEdit_3.setDisabled(True) 
            df.loc[df['PARAMETER'] == 'MIRR', 'VALUE'] = 'False'
        
        if debug:
            print(df)
               
    def changestate_interp(self):
        global debug
        
        if (self.checkBox_5.isChecked()):
            self.lineEdit_10.setDisabled(False)
            self.pushButton_6.setDisabled(False)
            df.loc[df['PARAMETER'] == 'INTERP', 'VALUE'] = 'True'
        else:
            self.lineEdit_10.setDisabled(True)
            self.pushButton_6.setDisabled(True)
            df.loc[df['PARAMETER'] == 'INTERP', 'VALUE'] = 'False'
            
        if debug:
            print(df)
 
    def changestate_checkwavelet(self):
        global debug
        
        if (self.checkBox_wavelet.isChecked()):
            self.lineEdit_wavelet.setDisabled(False)
            self.pushButton_wavelet.setDisabled(False)
            df.loc[df['PARAMETER'] == 'CONV', 'VALUE'] = 'True'
        else:
            self.lineEdit_wavelet.setDisabled(True)
            self.pushButton_wavelet.setDisabled(True)
            df.loc[df['PARAMETER'] == 'CONV', 'VALUE'] = 'False'
            
        if debug:
            print(df) 
 
    def changestate_checkdbl(self):
        global debug
        
        if (self.checkBox_dbl.isChecked()):
            df.loc[df['PARAMETER'] == 'DBL', 'VALUE'] = 'True'
            self.lineEdit_dbl2a.setDisabled(False)
            self.lineEdit_dbl2b.setDisabled(False)
            self.lineEdit_dbl3a.setDisabled(False)
            self.lineEdit_dbl3b.setDisabled(False)
            self.lineEdit_dbl4a.setDisabled(False)
            self.lineEdit_dbl4b.setDisabled(False)
            self.lineEdit_dbl5a.setDisabled(False)
            self.lineEdit_dbl5b.setDisabled(False)
            self.lineEdit_dbl6a.setDisabled(False)
        else:
            df.loc[df['PARAMETER'] == 'DBL', 'VALUE'] = 'False'
            self.lineEdit_dbl2a.setDisabled(True)
            self.lineEdit_dbl2b.setDisabled(True)
            self.lineEdit_dbl3a.setDisabled(True)
            self.lineEdit_dbl3b.setDisabled(True)
            self.lineEdit_dbl4a.setDisabled(True)
            self.lineEdit_dbl4b.setDisabled(True)
            self.lineEdit_dbl5a.setDisabled(True)
            self.lineEdit_dbl5b.setDisabled(True)
            self.lineEdit_dbl6a.setDisabled(True)
            
        if debug:
            print(df)     
 
    
    def changestate_wbsaf(self,text):
        global df, debug
        
        df.loc[df['PARAMETER'] == 'HORSAF', 'VALUE'] = text
        if debug:
            print(df)                         
                          
    def changestate_workflow(self,text):
        global df, debug
        
        df.loc[df['PARAMETER'] == 'ATYPE', 'VALUE'] = text
        if debug:
            print(df)
 
    def changestate_pool(self,text):
        global df, debug
        
        df.loc[df['PARAMETER'] == 'POOL', 'VALUE'] = text
        if debug:
            print(df)
                            
    def changestate_srctype(self,text):
        global df, debug
        
        if (text == "Mixed"):
             self.lineEdit_shtcod.setDisabled(False)
        else:
             self.lineEdit_shtcod.setDisabled(True)
   
        df.loc[df['PARAMETER'] == 'SRCTYPE', 'VALUE'] = text
        
        if debug:
            print(df)
        
    def changestate_shtcod(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'SHTCOD', 'VALUE'] = text
        if debug:
            print(df)          
        
    def changestate_jobrev(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'JOBREV', 'VALUE'] = text
        if debug:
            print(df)  
     
    def changestate_spssrc(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'SPSSRC', 'VALUE'] = text
        if debug:
            print(df)  
            
    def changestate_wavelet(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'WAVELET', 'VALUE'] = text
        if debug:
            print(df)   
        
    def changestate_spsrec(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'SPSREC', 'VALUE'] = text
        if debug:
            print(df)   

    def changestate_spsrel(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'SPSREL', 'VALUE'] = text
        if debug:
            print(df)  

    def changestate_x0(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'X0', 'VALUE'] = text
        if debug:
            print(df)  

    def changestate_y0(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'Y0', 'VALUE'] = text
        if debug:
            print(df)          

    def changestate_mirrz(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'MIRRZ', 'VALUE'] = text
        if debug:
            print(df)            
     
    def changestate_recip(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'RECIP', 'VALUE'] = text
        if debug:
            print(df)      

    def changestate_noisepre(self):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'NOISEAPP', 'VALUE'] = 'PRE'
        if debug:
            print(df)         
 
    def changestate_noisepos(self):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'NOISEAPP', 'VALUE'] = 'POS'
        if debug:
            print(df)      
 
    def changestate_noisemod(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'NOISEMODE', 'VALUE'] = text
        if debug:
            print(df) 
                
    def changestate_faclev(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'FACLEV', 'VALUE'] = text
        if debug:
            print(df) 
 
    def changestate_flow(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'FLOW', 'VALUE'] = text
        if debug:
            print(df) 
 
    def changestate_iorlow(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'IORLOW', 'VALUE'] = text
        if debug:
            print(df) 
    
    def changestate_fhigh(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'FHIGH', 'VALUE'] = text
        if debug:
            print(df)                            
 
    def changestate_iorhig(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'IORHIG', 'VALUE'] = text
        if debug:
            print(df)     
 
    def changestate_tmax(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'TMAX', 'VALUE'] = text
        if debug:
            print(df)      
 
    def changestate_dt(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'DT', 'VALUE'] = text
        if debug:
            print(df)    
 
    def changestate_tout(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'TOUT', 'VALUE'] = text
        if debug:
            print(df)    
     
    def changestate_t0(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'T0', 'VALUE'] = text
        if debug:
            print(df)
        
    def changestate_outdir(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'OUTDIR', 'VALUE'] = text
        if debug:
            print(df)       
        
    def changestate_ssf(self,text):
        global df, debug
   
        if (self.checkBox_3.isChecked()):
             df['SSF'] = 'True'
             df.loc[df['PARAMETER'] == 'SSF', 'VALUE'] = 'True'
        else:
             df.loc[df['PARAMETER'] == 'SSF', 'VALUE'] = 'False'
    
        if debug:
            print(df)       

    def changestate_qcgeom(self,text):
        global df, debug
   
        if (self.checkBox_6.isChecked()):
             df.loc[df['PARAMETER'] == 'QCGEOM', 'VALUE'] = 'True'
        else:
             df.loc[df['PARAMETER'] == 'QCGEOM', 'VALUE'] = 'False'
    
        if debug:
            print(df)       
 
    def changestate_qctime(self,text):
        global df, debug
   
        if (self.checkBox_7.isChecked()):
             df.loc[df['PARAMETER'] == 'QCTIME', 'VALUE'] = 'True'
        else:
             df.loc[df['PARAMETER'] == 'QCTIME', 'VALUE'] = 'False'
    
        if debug:
            print(df)  
 
    def changestate_qcdepth(self,text):
        global df, debug
   
        if (self.checkBox_8.isChecked()):
             df.loc[df['PARAMETER'] == 'QCDEPTH', 'VALUE'] = 'True'
        else:
             df.loc[df['PARAMETER'] == 'QCDEPTH', 'VALUE'] = 'False'
    
        if debug:
            print(df)

    def changestate_sqsaf(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'SQSORT', 'VALUE'] = text
        if debug:
            print(df)       

    def changestate_srtall(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'SRTALL', 'VALUE'] = text
        if debug:
            print(df) 

    def changestate_fmax(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'FMAX', 'VALUE'] = text
        if debug:
            print(df)   

    def changestate_ndip(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'NDIP', 'VALUE'] = text
        if debug:
            print(df)              

    def changestate_pmax(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'PMAX', 'VALUE'] = text
        if debug:
            print(df) 

    def changestate_mxblnd(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'MXBLND', 'VALUE'] = text
        if debug:
            print(df) 

    def changestate_xywindow(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'XYWINDOW', 'VALUE'] = text
        if debug:
            print(df) 

    def changestate_twindow(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'TWINDOW', 'VALUE'] = text
        if debug:
            print(df) 

    def changestate_niters(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'NITERS', 'VALUE'] = text
        if debug:
            print(df) 
 
    def changestate_nshot(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'NSHOT', 'VALUE'] = text
        if debug:
            print(df)              
 
    def changestate_nwavit(self,text):
        global df, debug
   
        df.loc[df['PARAMETER'] == 'NWAVIT', 'VALUE'] = text
        if debug:
            print(df) 
            
    def nextId(self):
        
        print('nextId')
        
        if self.pushButton_1s.clicked:
            val = 3       
            print ('pushed',val)
        elif self.pushButton_2s.clicked:
            val = 4       
            print ('pushed',val)
        else:
            val =  Wizard.currentId() + 1
            print (val)

        return val

    #----------------------------------------------------------------------
    #  SIDEBAR NEXT BUTTON ACTIONS
    #---------------------------------------------------------------------- 
    def nxtpage(self):
        global debug, icons
        
        if debug:
            print("nextpage = ",Wizard.currentId())
     
        # highlight the next button  
        if Wizard.currentId() == 2:
            self.pushButton_1s.setIcon(QIcon(icons[2]))
            self.pushButton_2s.setIcon(QIcon(icons[1]))
        elif Wizard.currentId() == 3:
            self.pushButton_2s.setIcon(QIcon(icons[2]))
            self.pushButton_3s.setIcon(QIcon(icons[1]))
        elif Wizard.currentId() == 4:
            self.pushButton_3s.setIcon(QIcon(icons[2]))
            self.pushButton_4s.setIcon(QIcon(icons[1])) 
        elif Wizard.currentId() == 5:
            self.pushButton_4s.setIcon(QIcon(icons[2]))
            self.pushButton_5s.setIcon(QIcon(icons[1]))
        elif Wizard.currentId() == 6:
            self.pushButton_5s.setIcon(QIcon(icons[2]))
            self.pushButton_6s.setIcon(QIcon(icons[1]))
        elif Wizard.currentId() == 7:
            self.pushButton_6s.setIcon(QIcon(icons[2]))
            self.pushButton_7s.setIcon(QIcon(icons[1]))
        elif Wizard.currentId() == 8:
            self.pushButton_7s.setIcon(QIcon(icons[2]))
            self.pushButton_8s.setIcon(QIcon(icons[1]))

    #----------------------------------------------------------------------
    #  SIDEBAR BACK BUTTON ACTIONS
    #---------------------------------------------------------------------- 
    def bckpage(self):
        global debug, icons
        
        if debug:
            print("previous page = ",Wizard.currentId())
            
        if Wizard.currentId() == 1:
            self.pushButton_1s.setIcon(QIcon(icons[1]))
            self.pushButton_2s.setIcon(QIcon(icons[2]))
        elif Wizard.currentId() == 2:
            self.pushButton_2s.setIcon(QIcon(icons[1]))
            self.pushButton_3s.setIcon(QIcon(icons[2]))
        elif Wizard.currentId() == 3:
            self.pushButton_3s.setIcon(QIcon(icons[1]))
            self.pushButton_4s.setIcon(QIcon(icons[2]))
        elif Wizard.currentId() == 4:
            self.pushButton_4s.setIcon(QIcon(icons[1]))
            self.pushButton_5s.setIcon(QIcon(icons[2])) 
        elif Wizard.currentId() == 5:
            self.pushButton_5s.setIcon(QIcon(icons[1]))
            self.pushButton_6s.setIcon(QIcon(icons[2]))
        elif Wizard.currentId() == 6:
            self.pushButton_6s.setIcon(QIcon(icons[1]))
            self.pushButton_7s.setIcon(QIcon(icons[2]))
        elif Wizard.currentId() == 7:
            self.pushButton_7s.setIcon(QIcon(icons[1]))
            self.pushButton_8s.setIcon(QIcon(icons[2]))

        
    def changestate_noise(self,text):
        global df, debug
        
        if (self.checkBox_5b.isChecked()):
             self.comboBox_3b.setDisabled(False)
             self.radioButton_1.setDisabled(False) 
             self.radioButton_2.setDisabled(False) 
             self.lineEdit_faclev.setDisabled(False)
             self.lineEdit_flow.setDisabled(False)
             self.lineEdit_iorlow.setDisabled(False)
             self.lineEdit_fhigh.setDisabled(False)
             self.lineEdit_iorhig.setDisabled(False)
             df.loc[df['PARAMETER'] == 'NOISE', 'VALUE'] = 'True'
        else:
             self.comboBox_3b.setDisabled(True)
             self.radioButton_1.setDisabled(True) 
             self.radioButton_2.setDisabled(True) 
             self.lineEdit_faclev.setDisabled(True)
             self.lineEdit_flow.setDisabled(True)
             self.lineEdit_iorlow.setDisabled(True)
             self.lineEdit_fhigh.setDisabled(True)
             self.lineEdit_iorhig.setDisabled(True)
             df.loc[df['PARAMETER'] == 'NOISE', 'VALUE'] = 'False'
             
        if debug:
            print(df)
     
    def closeout(self):
        msg = QMessageBox()
        msg.setWindowIcon(QtGui.QIcon("img/task-complete.png"))
        msg.setText("Success, build complete.")
        msg.setWindowTitle("Build Status")
        #msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok)
        return msg.exec() 

    def checkexistmess(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Files already exist.  Overwite (y/n)?")
        msg.setWindowTitle("Files Exist")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        return msg.exec()                  

    #----------------------------------------------------------------------
    #  HELP DIALOG
    #----------------------------------------------------------------------         
    def providehelp(self):
        global Dialog

        if Dialog is None:
            # show help window  
            Dialog = QtWidgets.QDialog()
            ui = helpgui.Ui_Dialog()
            ui.setupUi(Dialog)
            Dialog.setWindowTitle("Help for SimWiz")
            Dialog.show()
            Dialog.exec_() 
            Dialog = None 
            
    #----------------------------------------------------------------------
    #  COMPLETION DIALOG
    #----------------------------------------------------------------------  
    def done(self):
        global df, debug, Dialog
        
        # save pandas dataframe with wizard parameters
        filename = str(df.loc[3,"VALUE"]) + "-simwiz.csv" 
        fullpath = os.path.join(r'user',filename)
       
        # first check to see if the file exists
        if os.path.isfile(fullpath):           
            # print warning message
            choice = self.checkexistmess()
            if choice == 16384:
                build.buildmain(self,df,debug,fullpath)
            else:
                print('just quit')          
        else:
            build.buildmain(self,df,debug,fullpath)
            
        # make sure to close help dialog if one was opened
        if not Dialog == None:
            Dialog.close()
 
#------------------------------------------------------------------------------
#  MAIN
#------------------------------------------------------------------------------
#import backimage_rc
#import resource

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    Wizard = QtWidgets.QWizard()
    ui = Ui_Wizard()
    ui.setupUi(Wizard)
    Wizard.show()

    sys.exit(app.exec_())

