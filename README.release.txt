UPDATES IN THIS RELEASE
-----------------------

18/03/2022
----------

- Added ident ranging options to the output opions tab.  Three idents can be used to range the input data.
Note that the ranging only applies to the skeletons 02, 03 and 04.  Along with 05 and 06 these skeletons can be placed in
a multi-segment partition.  It is assumed that any attribute parameters have previously been defined e.g. $shtpt.

- SHT now is updated by SHTST (for normal geometry) or RECST (for reciprocal geometry).  Therefore there is not need to pass in
a unique shot number to the skeletons.  


01/02/2022
-------------

- Installed a private installation of Anaconda to avoid issues with Shell IT

- Added a desciption textbox on the intro page so that user comments can be captured

- Re-identing for key idents has been added as a user option

- Added a development library option so that users can test the non-production version

- SHTLIN/SHTPT idents added to data ranging

- Source split ident field added, so that ranging for spliting of mixed source data is now user controlled.

- OBNPTY skeleton edited to remove trace length TMAXS parameter