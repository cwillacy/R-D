# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 10:52:43 2021

@author: Christopher.Willacy
"""

import os
import platform
import subprocess
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication

#------------------------------------------------------------------------------
#
#  main module for starting the workflow build
#
#------------------------------------------------------------------------------
def buildmain(self, df, debug, fullpath):
        
    # start the busy cursor
    QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
 
    self.bar.setValue(0)
       
    # preserve string on output
    df = df.astype(str)

    # # save to csv file
    # df.to_csv(fullpath, index=False)

    # build skeletons
    # first create the include file
    buildinclude(self,df)
 
    self.bar.setValue(10)    
 
    if debug:
        print(str(df.loc[1,"VALUE"]))

    if str(df.loc[1,"VALUE"]) == 'Single': 

        tobuild = ['01_pre_mod_sps.skl', '02_pre_mod_norm.skl', '03_pre_mod_recip.skl', 
           '04_pos_mod_comb.skl', '05_pos_bld_cont.skl', '06_pos_bld_dist.skl']
        
        if str(df.loc[29,"VALUE"]) == 'True':
            tobuild.append('pre_qc_geom.skl')
            
        if str(df.loc[30,"VALUE"]) == 'True':
            tobuild.append('pre_qc_time.skl')
            
        if str(df.loc[31,"VALUE"]) == 'True':
            tobuild.append('pre_qc_depth.skl')     
            
        if str(df.loc[37,"VALUE"]) == 'True':
            tobuild.append('dbl1_deblend_da.skl')   
            tobuild.append('dbl2_deblend.skl') 

        for skl in tobuild:
            buildskl_single(self,df,skl)
            mymess = 'skeleton built ->' + skl + '\n'
            self.textBox_log.insertPlainText(mymess)
            val = self.bar.value()
            self.bar.setValue(val+10)
        
    else:
        
        tobuild = ['01_pre_mod_sps.skl', '02_pre_mod_norm.skl', '03_pre_mod_recip.skl', 
                   '04_pre_mod_nsplit.skl', '05_pre_mod_rsplit.skl', '06_pos_mod_hfidt.skl',
                   '07_pos_mod_lfidt.skl', '08_pos_mod_mrg.skl', '09_pos_bld_cont.skl', 
                   '10_pos_bld_dist.skl']
        
        if str(df.loc[29,"VALUE"]) == 'True':
            tobuild.append('pre_qc_geom.skl')
            
        if str(df.loc[30,"VALUE"]) == 'True':
            tobuild.append('pre_qc_time.skl')
            
        if str(df.loc[31,"VALUE"]) == 'True':
            tobuild.append('pre_qc_depth.skl')  

        if str(df.loc[37,"VALUE"]) == 'True':
            tobuild.append('dbl1_deblend_da.skl')   
            tobuild.append('dbl2_deblend.skl') 

        for skl in tobuild:
            mymess = 'skeleton built ->' + skl + '\n'
            self.textBox_log.insertPlainText(mymess)
            buildskl_multi(self,df,skl)              
    
    
    # build the jobpro partitions and add skeletons to jobpro if on Linux
    if platform.system() == 'Linux':

        revision = df.loc[3,"VALUE"]

        nseg = ((int(df.loc[56,"VALUE"]) - int(df.loc[55,"VALUE"]))) / int(df.loc[64,"VALUE"]) + 1
        print(nseg)
        segment_list = []
        for i in range(int(nseg)):
            segname = 's' + str(i+1)
            segment_list.append(segname)

        ident_list = []


        if str(df.loc[52,"VALUE"]) != '': 
            ident_list.append('ident1minval')
            ident_list.append('ident1inc')
            ident_list.append('ident1maxval')
        
        
        print('indentlist = ',ident_list)
        
        basename = df.loc[63,"VALUE"]
        
        build_jpcli(self,df,basename,tobuild,revision,segment_list,ident_list)
   
    self.bar.setValue(100)   
    # stop the busy cursor
    QApplication.restoreOverrideCursor()          
    # print out a completed message
    self.closeout()
    
    if debug:
        print("we are done") 
        
    return

#------------------------------------------------------------------------------
#
#  build the skl global include file
#
#------------------------------------------------------------------------------
def buildinclude(self,df):

     filename = str(df.loc[3,"VALUE"]) + "-simwiz_include.inc" 
     
     mypath = str(df.loc[27,"VALUE"])
     fullpath = os.path.join(mypath,filename)
     
     if not mypath:  
        # check which os we are on
        if platform.system() == 'Windows':
           # check to see if directory exists
           MYDIR = (r"c:\apps\SimWiz-store\skeletons")
           CHECK_FOLDER = os.path.isdir(MYDIR)
           if not CHECK_FOLDER:
               os.makedirs(MYDIR)
      
           fullpath = os.path.join(MYDIR,filename)
        else:
            MYDIR = os.path.expanduser('~/SimWiz-store/skeletons')            
            CHECK_FOLDER = os.path.isdir(MYDIR)
            if not CHECK_FOLDER:
               os.makedirs(MYDIR)
            
            fullpath = os.path.join(MYDIR,filename)
               
     else:
         fullpath = os.path.join(mypath,filename)

     file = open(fullpath,'w')
     file.write("&!---------------------------------------------\n")
     file.write("&!  include file for " + str(df.loc[3,"VALUE"]) + " generated by SimWiz \n")
     file.write("&!---------------------------------------------\n")
     file.write('& character spssrc_wiz = ' + '\'' + df.loc[4,"VALUE"] + '\'' + '\n')
     file.write('& character spsrec_wiz = ' + '\'' + df.loc[5,"VALUE"] + '\'' + '\n')
     file.write('& character spsrel_wiz = ' + '\'' + df.loc[6,"VALUE"] + '\'' + '\n')
     file.write('& integer sqsort_wiz = ' + str(df.loc[32,"VALUE"]) + '\n')
     file.write('& integer srtall_wiz = ' + str(df.loc[33,"VALUE"]) + '\n')
     boolval = str(df.loc[7,"VALUE"])
     file.write('& boolean xyshift_wiz = ' + boolval.lower() + '\n')
     file.write('& integer x0_wiz = ' + str(df.loc[8,"VALUE"]) + '\n')
     file.write('& integer y0_wiz = ' + str(df.loc[9,"VALUE"]) + '\n')                     
     file.write('& character safsrc_wiz = ' + '\'' + str(df.loc[3,"VALUE"]) + '-sps_s' + '\'' + '\n')               
     file.write('& character safrec_wiz = ' + '\'' + str(df.loc[3,"VALUE"]) + '-sps_r' + '\'' + '\n')
     file.write('& character safrel_wiz = ' + '\'' + str(df.loc[3,"VALUE"]) + '-sps_x' + '\'' + '\n')
     boolval = str(df.loc[28,"VALUE"])
     file.write('& boolean ssf_wiz = ' + boolval.lower() + '\n')
     boolval = str(df.loc[13,"VALUE"])
     file.write('& boolean interp_wiz = ' + boolval.lower() + '\n')
     file.write('& character horsaf_wiz = ' + '\'' + str(df.loc[14,"VALUE"]) + '\'' + '\n')
     boolval = str(df.loc[10,"VALUE"])
     file.write('& boolean mirr_wiz = ' + boolval.lower() + '\n')
     myfloat = str(float(df.loc[11,"VALUE"]))
     file.write('& real mirrz_wiz = ' + myfloat + '\n')
     boolval = str(df.loc[34,"VALUE"])
     file.write('& boolean conv_wiz = ' + boolval.lower() + '\n')
     file.write('& character wavelet_wiz = ' + '\'' + str(df.loc[35,"VALUE"]) + '\'' + '\n')
     file.write('& character orig_geom_wiz = ' + '\'' + str(df.loc[3,"VALUE"]) + '-sps_pre_saf' + '\'' + '\n')

     if str(df.loc[17,"VALUE"]) == 'PRE':       
         file.write('& boolean pre_noise_wiz = true \n')
     else:
         file.write('& boolean pre_noise_wiz = false \n') 

     file.write('& character noiseapp_wiz = ' + '\'' + str(df.loc[17,"VALUE"]) + '\'' + '\n')
     myfloat = str(float(df.loc[18,"VALUE"]))
     file.write('& real faclev_wiz = ' + myfloat + '\n')
     myfloat = str(float(df.loc[19,"VALUE"]))
     file.write('& real flow_wiz = ' + myfloat + '\n')
     myfloat = str(float(df.loc[21,"VALUE"]))
     file.write('& real fhigh_wiz = ' + myfloat + '\n')
     file.write('& integer iorlow_wiz = ' + str(df.loc[20,"VALUE"]) + '\n')
     file.write('& integer iorhig_wiz = ' + str(df.loc[22,"VALUE"]) + '\n')
     file.write('& character post_norm_wiz = ' + '\'' + str(df.loc[3,"VALUE"]) + '-pos_trc' + '\'' + '\n')
     file.write('& integer tmax_wiz = ' + str(df.loc[23,"VALUE"]) + '\n')
     file.write('& integer dt_wiz = ' + str(df.loc[24,"VALUE"]) + '\n')
     file.write('& integer tout_wiz = ' + str(df.loc[25,"VALUE"]) + '\n')
     file.write('& integer t0_wiz = ' + str(df.loc[26,"VALUE"]) + '\n')
     
     if str(df.loc[15,"VALUE"]) == 'False':
         file.write('& boolean pre_noise_wiz = false \n')
         file.write('& boolean pos_noise_wiz = false \n')
     else:
         if str(df.loc[17,"VALUE"]) == 'PRE':       
             file.write('& boolean pre_noise_wiz = true \n')
             file.write('& boolean pos_noise_wiz = false \n')
         else:
             file.write('& boolean pre_noise_wiz = false \n') 
             file.write('& boolean pos_noise_wiz = true \n')
     
     file.write('& integer shtcod_wiz = ' + str(df.loc[2,"VALUE"]) + '\n')
     file.write('& character orig_ssf_wiz = ' + '\'' + str(df.loc[3,"VALUE"]) + '-sps_pre_trc' + '\'' + '\n')
     file.write('& character blended_trc_wiz = ' + '\'' + str(df.loc[3,"VALUE"]) + '-blended_cont_trc' + '\'' + '\n')
     file.write('& character recip_geom_wiz = ' + '\'' + str(df.loc[3,"VALUE"]) + '-sps_pre_rcp_saf' + '\'' + '\n')
     file.write('& character recip_ssf_wiz = ' + '\'' + str(df.loc[3,"VALUE"]) + '-sps_pre_rcp_trc' + '\'' + '\n')
            
 
     if str(df.loc[1,"VALUE"]) == 'Mixed':
         file.write('& character hfsplit_saf_wiz = ' + '\'' + str(df.loc[3,"VALUE"]) + '-hfsplit_saf' + '\'' + '\n')
         file.write('& character lfsplit_saf_wiz = ' + '\'' + str(df.loc[3,"VALUE"]) + '-lfsplit_saf' + '\'' + '\n')
         file.write('& character pos_norm_hftrc_wiz = ' + '\'' + str(df.loc[3,"VALUE"]) + '-pos_hftrc' + '\'' + '\n')
         file.write('& character pos_norm_lftrc_wiz = ' + '\'' + str(df.loc[3,"VALUE"]) + '-pos_lftrc' + '\'' + '\n')
         file.write('& character post_norm_wiz = ' + '\'' + str(df.loc[3,"VALUE"]) + '-pos_mrg_trc' + '\'' + '\n')
     else:
         file.write('& character post_norm_wiz = ' + '\'' + str(df.loc[3,"VALUE"]) + '-pos_trc' + '\'' + '\n')
         
     file.write('& character pool_wiz = ' + '\'' + str(df.loc[36,"VALUE"]) + '\'' + '\n')
     file.write('& character pos_saf_wiz = ' + '\'' + str(df.loc[3,"VALUE"]) + '-pos_blend_saf' + '\'' + '\n')
     file.write('& integer dbl_fmax_wiz = ' + str(df.loc[38,"VALUE"]) + '\n')
     file.write('& integer dbl_ndip_wiz = ' + str(df.loc[39,"VALUE"]) + '\n')
     myfloat = str(float(df.loc[40,"VALUE"]))
     file.write('& real dbl_pmax_wiz = ' + myfloat + '\n')
     file.write('& integer dbl_mxblnd_wiz = ' + str(df.loc[41,"VALUE"]) + '\n')    
     file.write('& integer dbl_xywindow_wiz = ' + str(df.loc[42,"VALUE"]) + '\n')   
     file.write('& integer dbl_twindow_wiz = ' + str(df.loc[43,"VALUE"]) + '\n') 
     file.write('& integer dbl_niters_wiz = ' + str(df.loc[44,"VALUE"]) + '\n') 
     file.write('& integer dbl_nshot_wiz = ' + str(df.loc[45,"VALUE"]) + '\n') 
     file.write('& integer dbl_nwavit_wiz = ' + str(df.loc[46,"VALUE"]) + '\n') 
     
     if str(df.loc[12,"VALUE"]) == 'True':       
         file.write('& boolean recip_wiz = true \n')
     else:
         file.write('& boolean recip_wiz = false \n')
         
     file.write('& character da_residual_trc_wiz = ' + '\'' + str(df.loc[3,"VALUE"]) + '-da_residual' + '\'' + '\n')    
     file.write('& character da_deblend_trc_wiz = ' + '\'' + str(df.loc[3,"VALUE"]) + '-da_deblend' + '\'' + '\n')
      
     if str(df.loc[47,"VALUE"]) == 'True':       
          file.write('& boolean reident_wiz = True \n')
     else:
          file.write('& boolean reident_wiz = False \n')
         
     if str(df.loc[48,"VALUE"]) == 'True':       
          file.write('& boolean dev_wiz = True \n')
     else:
          file.write('& boolean dev_wiz = False \n')
 
     file.write('& character splitident_wiz = ' + '\'' + str(df.loc[50,"VALUE"]) + '\'' + '\n')
           
     mystring = '& character description_wiz = ' 
     
     mystring = mystring + '\'' 
     
     mystring2 = str(df.loc[49,"VALUE"]).replace('\n','\\n')
     
     mystring = mystring + mystring2
     
     mystring = mystring + '\'\n'
     
     file.write(mystring) 
     file.write('& character ident1_wiz = ' + '\'' + str(df.loc[52,"VALUE"]) + '\'' + '\n')
     file.write('& integer ident1minval_wiz = ' + str(df.loc[55,"VALUE"]) + '\n')
     file.write('& integer ident1maxval_wiz = ' + str(df.loc[56,"VALUE"]) + '\n')
     
     file.write('& character ident2_wiz = ' + '\'' + str(df.loc[53,"VALUE"]) + '\'' + '\n')
     file.write('& integer ident2minval_wiz = ' + str(df.loc[57,"VALUE"]) + '\n')
     file.write('& integer ident2maxval_wiz = ' + str(df.loc[58,"VALUE"]) + '\n')
     
     file.write('& character ident3_wiz = ' + '\'' + str(df.loc[54,"VALUE"]) + '\'' + '\n')
     file.write('& integer ident3minval_wiz = ' + str(df.loc[59,"VALUE"]) + '\n')
     file.write('& integer ident3maxval_wiz = ' + str(df.loc[60,"VALUE"]) + '\n')
     file.write('& integer ident1inc_wiz = ' + str(df.loc[64,"VALUE"]) + '\n')
     file.write('& integer ident2inc_wiz = ' + str(df.loc[65,"VALUE"]) + '\n')
     file.write('& integer ident3inc_wiz = ' + str(df.loc[66,"VALUE"]) + '\n')
          
     file.close()
     
     # display the simwiz paarmeter file to the log
     # no we are ready to launch the job to build partitions etc
     
     with open(fullpath) as f:
          for line in f:
              print(line)
              self.textBox_log.insertPlainText(line)
     
     f.close()
     
     self.textBox_log.centerCursor()
         
     return
 
#------------------------------------------------------------------------------
#
#  build the skl's for a single source type workflow
#
#------------------------------------------------------------------------------
def buildskl_single(self,df,skl):

   filename = skl
   include_file = '\'' + str(df.loc[3,"VALUE"]) + '-simwiz_include.inc' + '\'' 
   
   if platform.system() == 'Linux':
       fullpath = os.path.join(r'templates/single',filename)
   else:
       fullpath = os.path.join(r'templates\single',filename)
  
   filename_skl = str(df.loc[3,"VALUE"]) + '-' + filename
   mypath = str(df.loc[27,"VALUE"])
   
   if not mypath:  
        # check which os we are on
        if platform.system() == 'Windows':
            # check to see if directory exists
            MYDIR = (r"c:\apps\SimWiz-store\skeletons")
            fullpath_skl = os.path.join(MYDIR,filename_skl)
        else:
            MYDIR = os.path.expanduser('~/SimWiz-store/skeletons')
            fullpath_skl = os.path.join(MYDIR,filename_skl)
              
   else:
         fullpath_skl = os.path.join(mypath,filename_skl)   

   file = open(fullpath_skl,'w')        
      
   with open(fullpath,'r') as f:
       for line in f:
           if '#######' in line:
               file.write(line.replace('#######',include_file))
           elif '~~~' in line:
               if str(df.loc[48,"VALUE"]) == 'True':   
                   file.write(line.replace('~~~','dev'))
               else:
                   file.write(line.replace('~~~','cur'))    
           elif '@@@' in line:
               
               
               if str(df.loc[52,"VALUE"]) != '' and str(df.loc[53,"VALUE"]) == '' and str(df.loc[54,"VALUE"]) == '':
                   
                   input_str = """& call io:sqsaf_in(sqsaf => {                &
&    data_set => receiver_input,             &
&    exec => 'EXEC',                         &
&    media => {                              &
&       data_range => ({                     &
&          mnemon => 'RECST',                &
&          minval => $ident1minval,          &
&          incr => $ident1inc,               &
&          maxval => $ident1maxval           &
&       })                                   &
&    }                                       &
& },                                         &
&                  mode => 'DECLARE+CARDS')"""

                   
               elif str(df.loc[52,"VALUE"]) != '' and str(df.loc[53,"VALUE"]) != '' and str(df.loc[54,"VALUE"]) == '':
                     
                    input_str = """& call io:sqsaf_in(sqsaf => {                &
&    data_set => receiver_input,             &
&    exec => 'EXEC',                         &
&    media => {                              &
&       data_range => ({                     &
&          mnemon => ident1_wiz,             &
&          minval => $iden1minval,           &   
&          incr => $ident1inc,               &
&          maxval => $ident1maxval           &
&       }, {                                 &
&          mnemon => ident2_wiz,             &
&          minval => $ident2minval,          &
&          incr => $ident2inc,               &
&          maxval => $ident2maxval           &
&       })                                   &
&    }                                       &
& },                                         &
&                  mode => 'DECLARE+CARDS')"""
                   
                   
               elif str(df.loc[52,"VALUE"]) != '' and str(df.loc[53,"VALUE"]) != '' and str(df.loc[54,"VALUE"]) != '':   
                   
                    input_str = """& call io:sqsaf_in(sqsaf => {                &
&    data_set => receiver_input,             &
&    exec => 'EXEC',                         &
&    media => {                              &
&       data_range => ({                     &
&          mnemon => ident1_wiz,             &
&          minval => $iden1minval,           &
&          incr => $ident1inc,               &
&          maxval => $ident1maxval           &
&       }, {                                 &
&          mnemon => ident2_wiz,             &
&          minval => $ident2minval,          &
&          incr => $ident2inc,               &
&          maxval => $ident2maxval           &
&       }, {                                 &
&          mnemon => ident3_wiz,             &
&          minval => $ident3minval,          &
&          incr => $ident3inc,               &
&          maxval => $ident3maxval           &
&       })                                   &
&    }                                       &
& },                                         &
&                  mode => 'DECLARE+CARDS')"""


               else:
                       
                    input_str = """& call io:sqsaf_in(sqsaf => {                &
&    data_set => receiver_input,             &
&    exec => 'EXEC'                          &
& },                                         &
&                  mode => 'DECLARE+CARDS')"""

                               
               file.write(line.replace('@@@',input_str))

           elif '*~*' in line:
               
               
               if str(df.loc[52,"VALUE"]) != '' and str(df.loc[53,"VALUE"]) == '' and str(df.loc[54,"VALUE"]) == '':
                   
                   input_str = """& call io:sipmap_in(sipmap => {         &
&    data_set => ssf_input,                  &
&    media => {                              &
&       data_range => ({                     &
&          mnemon => ident1_wiz,             &
&          minval => $ident1minval,          &
&          incr => $ident1inc,               &
&          maxval => $ident1maxval           &
&       })                                   &
&    }                                       &
& },                                         &
&                  mode => 'DECLARE')"""

                   
               elif str(df.loc[52,"VALUE"]) != '' and str(df.loc[53,"VALUE"]) != '' and str(df.loc[54,"VALUE"]) == '':
                     
                    input_str = """& call io:sipmap_in(sipmap => {         &
&    data_set => ssf_input,                  &
&    media => {                              &
&       data_range => ({                     &
&          mnemon => ident1_wiz,             &
&          minval => $iden1minval,           &
&          incr => $ident1inc_wiz,           &
&          maxval => $ident1maxval_wiz       &
&       }, {                                 &
&          mnemon => ident2_wiz,             &
&          minval => $ident2minval,          &
&          incr => $ident2inc,               &
&          maxval => $ident2maxval           &
&       })                                   &
&    }                                       &
& },                                         &
&                  mode => 'DECLARE')"""
                   
                   
               elif str(df.loc[52,"VALUE"]) != '' and str(df.loc[53,"VALUE"]) != '' and str(df.loc[54,"VALUE"]) != '':   
                   
                    input_str = """& call io:sipmap_in(sipmap => {         &
&    data_set => ssf_input,                  &
&    media => {                              &
&       data_range => ({                     &
&          mnemon => ident1_wiz,             &
&          minval => $iden1minval,           &
&          incr => $ident1inc,               &
&          maxval => $ident1maxval           &
&       }, {                                 &
&          mnemon => ident2_wiz,             &
&          minval => $ident2minval,          &
&          incr => $ident2inc,               &
&          maxval => $ident2maxval           &
&       }, {                                 &
&          mnemon => ident3_wiz,             &
&          minval => $ident3minval,          &
&          incr => $ident3inc,               &
&          maxval => $ident3maxval           &
&       })                                   &
&    }                                       &
& },                                         &
&                  mode => 'DECLARE')"""


               else:
                       
                    input_str = """& call io:sipmap_in(sipmap => {         &
&    data_set => ssf_input                   &
& },                                         &
&                  mode => 'DECLARE')"""

                               
               file.write(line.replace('*~*',input_str))

           elif ':;' in line:
               
               
               if str(df.loc[52,"VALUE"]) != '' and str(df.loc[53,"VALUE"]) == '' and str(df.loc[54,"VALUE"]) == '':
                   
                   input_str = """& call io:sipmap_in(sipmap => {         &
&    data_set => ssf_input,                  &
&    media => {                              &
&       data_range => ({                     &
&          mnemon => ident1_wiz,             &
&          minval => $ident1minval,          &
&          incr => $ident1inc,               &
&          maxval => $ident1maxval           &
&       })                                   &
&    }                                       &
& },                                         &
&                  mode => 'CARDS')"""

                   
               elif str(df.loc[52,"VALUE"]) != '' and str(df.loc[53,"VALUE"]) != '' and str(df.loc[54,"VALUE"]) == '':
                     
                    input_str = """& call io:sipmap_in(sipmap => {         &
&    data_set => ssf_input,                  &
&    media => {                              &
&       data_range => ({                     &
&          mnemon => ident1_wiz,             &
&          minval => $iden1minval,           &
&          incr => $ident1inc,               &
&          maxval => $ident1maxval           &
&       }, {                                 &
&          mnemon => ident2_wiz,             &
&          minval => $ident2minval,          &
&          incr => $ident2inc,               &
&          maxval => $ident2maxval           &
&       })                                   &
&    }                                       &
& },                                         &
&                  mode => 'CARDS')"""
                   
                   
               elif str(df.loc[52,"VALUE"]) != '' and str(df.loc[53,"VALUE"]) != '' and str(df.loc[54,"VALUE"]) != '':   
                   
                    input_str = """& call io:sipmap_in(sipmap => {         &
&    data_set => ssf_input,                  &
&    media => {                              &
&       data_range => ({                     &
&          mnemon => ident1_wiz,             &
&          minval => $iden1minval,           &
&          incr => $ident1inc,               &
&          maxval => $ident1maxval           &
&       }, {                                 &
&          mnemon => ident2_wiz,             &
&          minval => $ident2minval,          &
&          incr => $ident2inc,               &
&          maxval => $ident2maxval_wiz       &
&       }, {                                 &
&          mnemon => ident3_wiz,             &
&          minval => $ident3minval,          &
&          incr => $ident3inc,               &
&          maxval => $ident3maxval           &
&       })                                   &
&    }                                       &
& },                                         &
&                  mode => 'CARDS')"""


               else:
                       
                    input_str = """& call io:sipmap_in(sipmap => {         &
&    data_set => ssf_input                   &
& },                                         &
&                  mode => 'CARDS')"""

                               
               file.write(line.replace(':;',input_str))
                   
           else:
               file.write(line)
   
   file.close()
   
     
   
   return

#------------------------------------------------------------------------------
#
#  build the skl's for a multi-source type workflow
#
#------------------------------------------------------------------------------
def buildskl_multi(self,df,skl):

    filename = skl
    include_file = '\'' + str(df.loc[3,"VALUE"]) + '-simwiz_include.inc' + '\'' 
    
    if platform.system() == 'Linux':
        fullpath = os.path.join(r'templates/multi',filename)
    else:
        fullpath = os.path.join(r'templates\multi',filename)
   
    filename_skl = str(df.loc[3,"VALUE"]) + '-' + filename
    mypath = str(df.loc[27,"VALUE"])
 
    if not mypath:  
         # check which os we are on
         if platform.system() == 'Windows':
             # check to see if directory exists
             MYDIR = (r"c:\apps\SimWiz-store\skeletons")
             fullpath_skl = os.path.join(MYDIR,filename_skl)
         else:
            MYDIR = os.path.expanduser('~/SimWiz-store/skeletons')
            fullpath_skl = os.path.join(MYDIR,filename_skl)              
    else:
          fullpath_skl = os.path.join(mypath,filename_skl)  
      
    file = open(fullpath_skl,'w')        
       
    with open(fullpath,'r') as f:
       for line in f:
           if '#######' in line:
               file.write(line.replace('#######',include_file))
           elif '~~~' in line:
               if str(df.loc[48,"VALUE"]) == 'True':   
                   file.write(line.replace('~~~','dev'))
               else:
                   file.write(line.replace('~~~','cur')) 
                   
           elif '@@@' in line:
               
               
               if str(df.loc[52,"VALUE"]) != '' and str(df.loc[53,"VALUE"]) == '' and str(df.loc[54,"VALUE"]) == '':
                   
                   input_str = """& call io:sqsaf_in(sqsaf => {                &
&    data_set => receiver_input,             &
&    exec => 'EXEC',                         &
&    media => {                              &
&       data_range => ({                     &
&          mnemon => 'RECST',                &
&          minval => $ident1minval,          &
&          incr => $ident1inc,               &
&          maxval => $ident1maxval           &
&       })                                   &
&    }                                       &
& },                                         &
&                  mode => 'DECLARE+CARDS')"""

                   
               elif str(df.loc[52,"VALUE"]) != '' and str(df.loc[53,"VALUE"]) != '' and str(df.loc[54,"VALUE"]) == '':
                     
                    input_str = """& call io:sqsaf_in(sqsaf => {                &
&    data_set => receiver_input,             &
&    exec => 'EXEC',                         &
&    media => {                              &
&       data_range => ({                     &
&          mnemon => ident1_wiz,             &
&          minval => $iden1minval,           &
&          incr => $ident1inc,               &
&          maxval => $ident1maxval           &
&       }, {                                 &
&          mnemon => ident2_wiz,             &
&          minval => $ident2minval,          &
&          incr => $ident2inc,               &
&          maxval => $ident2maxval           &
&       })                                   &
&    }                                       &
& },                                         &
&                  mode => 'DECLARE+CARDS')"""
                   
                   
               elif str(df.loc[52,"VALUE"]) != '' and str(df.loc[53,"VALUE"]) != '' and str(df.loc[54,"VALUE"]) != '':   
                   
                    input_str = """& call io:sqsaf_in(sqsaf => {                &
&    data_set => receiver_input,             &
&    exec => 'EXEC',                         &
&    media => {                              &
&       data_range => ({                     &
&          mnemon => ident1_wiz,             &
&          minval => $iden1minval,           &
&          incr => $ident1inc,               &
&          maxval => $ident1maxval           &
&       }, {                                 &
&          mnemon => ident2_wiz,             &
&          minval => $ident2minval,          &
&          incr => $ident2inc,               &
&          maxval => $ident2maxval           &
&       }, {                                 &
&          mnemon => ident3_wiz,             &
&          minval => $ident3minval,          &
&          incr => $ident3inc,               &
&          maxval => $ident3maxval           &
&       })                                   &
&    }                                       &
& },                                         &
&                  mode => 'DECLARE+CARDS')"""


               else:
                       
                    input_str = """& call io:sqsaf_in(sqsaf => {                &
&    data_set => receiver_input,             &
&    exec => 'EXEC'                          &
& },                                         &
&                  mode => 'DECLARE+CARDS')"""

                               
               file.write(line.replace('@@@',input_str))       
           else:
               file.write(line)
    
    file.close()
    return

#------------------------------------------------------------------------------
#
#  build the jobpro partition building script
#
#------------------------------------------------------------------------------
def build_jpcli(self,df,basename,tobuild,revision,segment_list,ident_list):

    library = str(df.loc[61,"VALUE"])    
    project = str(df.loc[62,"VALUE"]) 
    part1 = basename + '_ad1'
    part2 = basename + '_ad2'
        
    jobset_list = []
    for job in tobuild:
        skl = job.split('.')
        jobset_list.append(skl[0])
  
    # check to see if the partitions already exist
    jpcli_file = r'build/jpcli_check_part.txt'
     
    file = open(jpcli_file,'w')
    
    # define the add parition
    file.write('list_partition ' + part1 + ' library ' + library + ' project ' + project + ' outputfile build/jp_part_exist.txt' + '\n')
    
    file.close()
    
    os.system('jpcli < build/jpcli_check_part.txt')
    
    # now check the output to see if part exists or not
    fullpath = r'build/jp_part_exist.txt'
    found = 0       
    with open(fullpath) as f:
        for line in f:
            if part1 in line: 
                found = 1 
    f.close()              
    
    
    # build the jpcli command list
    jpcli_file = r'build/my_jpcli.txt'
 
    print(jpcli_file)
     
    file = open(jpcli_file,'w')
       
    if found == 0:
    
        # define the add parition
        file.write('add_partition ' + part1 + ' library ' + library + ' project ' + project + '\n')
        file.write('add_partition ' + part2 + ' library ' + library + ' project ' + project + '\n')
    
        # define the add jobset
        count = 0
        for jobset in jobset_list:
            if count == 0:
                file.write('add_jobset ' + jobset + ' revision ' + revision + ' library ' + library + ' project ' + project + ' partition ' + part1 + '\n')
            else:
                file.write('add_jobset ' + jobset + ' revision ' + revision + ' library ' + library + ' project ' + project + ' partition ' + part2 + '\n')
        
            count = count + 1
        
        # define add segments
        file.write('add_segment s1' + ' library ' + library + ' project ' + project + ' partition ' + part1 + '\n')
        for segment in segment_list:
          file.write('add_segment ' + segment + ' library ' + library + ' project ' + project + ' partition ' + part2 + '\n')
          
        # define add segment attributes
        for ident in ident_list:
            file.write('add_segment_attribute ' + ident + ' library ' + library + ' project ' + project + ' partition ' + part2 + ' default 1' + ' kind integer' + '\n')
        
        # update segment attributes with user values
        ident1minval = int(df.loc[55,"VALUE"])
        ident1inc = int(df.loc[64,"VALUE"])  
        ident1maxval = int(df.loc[64,"VALUE"]) 
                
        for segment in segment_list:
            if len(ident_list) == 3:
                file.write('update_segment_attribute ident1minval' + ' library ' + library + ' project ' + project + ' partition ' + part2 + ' segment ' + segment + ' value ' + str(ident1minval) + '\n')
                file.write('update_segment_attribute ident1inc' + ' library ' + library + ' project ' + project + ' partition ' + part2 + ' segment ' + segment + ' value ' + str(ident1inc) + '\n')
                file.write('update_segment_attribute ident1maxval' + ' library ' + library + ' project ' + project + ' partition ' + part2 + ' segment ' + segment + ' value ' + str(ident1minval) + '\n')    
                ident1minval = ident1minval + ident1inc  

    else:
        print('Partition already exists, will add to exsiting partition')
        # define the add jobset
        count = 0
        for jobset in jobset_list:
            if count == 0:
                file.write('add_jobset ' + jobset + ' revision ' + revision + ' library ' + library + ' project ' + project + ' partition ' + part1 + '\n')
            else:
                file.write('add_jobset ' + jobset + ' revision ' + revision + ' library ' + library + ' project ' + project + ' partition ' + part2 + '\n')
        
            count = count + 1
            
            
  
    file.close()  

    mymess = 'starting jpcli execution....' + '\n'
    self.textBox_log.insertPlainText(mymess)
    # no we are ready to launch the job to build partitions etc
    
    getOutput =  subprocess.Popen("jpcli < build/my_jpcli.txt", shell=True, stdout=subprocess.PIPE).stdout
    output =  getOutput.read()

    #print("My version is", output.decode())

    self.textBox_log.insertPlainText(output.decode())
    
    #os.system('jpcli < build/my_jpcli.txt')

    mymess = 'jpcli execution completed' + '\n'
    self.textBox_log.insertPlainText(mymess)
    self.textBox_log.centerCursor()
     
    return