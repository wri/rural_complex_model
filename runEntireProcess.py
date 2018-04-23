#####################################################################################
# Script to run all processing and analysis for PhD paper 1 - spatial patterns of SC
#   Giuseppe Molinario
#   09/17/2014
#   07/05/2014 update to extend to 2014
#   01/2018 - rerunning to include 2015. 
#
#   This script runs the following scripts:
#    1. Create directory structure
#    2. run LFT
#    3. Core grouping code
#    4. Fragmentation map build
#    5. Rural Complex Footprint map build
#    6. Intersect GFC and FACET loss and FF and RCF
#    7. Generate report tables by units of area (admin, pa, landscape)
#    8. Generate maps and animated gifs for illustrations
#    9. **Load tables in R, generate final tables and graphs *To do* (modify R scripts from PFL/SFL ratio analysis)**
#
######################################################################################

# Import
import arcpy
import os
from arcpy.sa import *
import shutil


version="18"


'''
##################################################
# Create and prepare root folder for run
##################################################

# Create root folder
rootFolder=version+"th_run"
# path
root=r"C:\Data_Molinario\temp\LFT_local"
# path with folder
rootFolderPath = root+"/"+rootFolder
# Create the folder if it doesn't exist
if not os.path.exists(rootFolderPath):
    os.makedirs(rootFolderPath)
    print "Created "+rootFolderPath+" folder."

# Copy over water and nodata folder from previous version, which does not change. 

# Source folder for Water and Nodata
src=root+"/"+str(int(version)-1)+"th_run"+"/"+r"Rural_complex_v5\WaterAndNodata"
# Destination folder
dst=rootFolderPath+"/"+r"Rural_complex_v5\WaterAndNodata"
if not os.path.exists(dst):
    shutil.copytree(src, dst)
    print "Copied over the water and noData folder."
else:
    print "Water and noData folder already exists in: "+dst



##################################################
# Run the LFT master mask creation
##################################################

# Location of build mask script 
buildMaster = ("C:\\Data_Molinario\\Dropbox\\PhD\\Scripts\\arcpyBuildInputMaskForLFT_v2.py")
print "python "+buildMaster
handle = os.system("python "+buildMaster)

print "Version: "+version+". Master mask input for LFT has been created."


##################################################
# Run the script to subtract NF and WD from outside the AOI
##################################################

# Location of the script
cleanMaster = ("C:\\Data_Molinario\\Dropbox\\PhD\\Scripts\\arcpyCleanMasterForLFTpostAOI.py")
print "python "+buildMaster
handle = os.system("python "+cleanMaster)

print "Version: "+version+". The master mask input for LFT has been cleaned so there is only SF/SFL/WDL outside AOI."



##################################################
# v16 07/2016
# Create the hybrid FACET/GFC masks
##################################################


# Location of the script to create the v16 folder structure and Master masks for LFT 
hybridMasters = ("C:\\Data_Molinario\\Dropbox\\PhD\\Scripts\\LFT\\arcpyBuildHybridFacetGFCInputMasksForLFT_v1.py")


print "python "+hybridMasters
handle = os.system("python "+hybridMasters)

print "Version: "+version+". New hybrid Master masks have been created and put into folder structure."




##################################################
# Run the batch LFT 
##################################################

#   also runs LFT_SA_gm_test_more_core_clss.py

# Location of the batch LFT script 
lftBatch = ("C:\\Data_Molinario\\Dropbox\\PhD\\Scripts\\LFT\\batchTiledLFT_v5.py")


print "python "+lftBatch
handle = os.system("python "+lftBatch)

print "Version: "+version+". LFT script has been run."


'''
#################################################
# Run the core group stratification
#################################################

# Location of script 
coreScript = ("C:\\Data_Molinario\\Dropbox\\PhD\\Scripts\\arcpyGroupCoreForestThresholds.py")

print "python "+ coreScript
handle = os.system("python "+coreScript)

print "Version: "+version+". Core classification has been run."

'''

################################################
# Run the add core to LFT script, make final forest fragmentation map
################################################

# Location of script 
addCoreToLftScript = ("C:\\Data_Molinario\\Dropbox\\PhD\\Scripts\\arcpyAddCorrectCoreToLFT.py")

print "python "+ addCoreToLftScript
handle = os.system("python "+addCoreToLftScript)

print "Version: "+version+". Core classification has been added to LFT "



################################################
# Run rural complex script
################################################

# Location of script 
ruralComplexScript = ("C:\\Data_Molinario\\Dropbox\\PhD\\Scripts\\arcpyCreateRuralComplex_v2.py")

print "python "+ ruralComplexScript
handle = os.system("python "+ruralComplexScript)

print "Version: "+version+". Rural complex classification has been created."


##################################################################
# Run the intersection of FACET and GFC loss with LFT and RC maps.
##################################################################

# Location of script 
lossIntersectionScript = ("C:\\Data_Molinario\\Dropbox\\PhD\\Scripts\\arcpyIntersectLFTandGFC_v3.py")

print "python "+ lossIntersectionScript
handle = os.system("python "+lossIntersectionScript)

print "Version: "+version+". Loss intersection with FF and RCF classification has been created."


#################################################################
##### Check maps before running tabulation and reporting of results 
#################################################################

# Set code to run or not
#tabulation = "yes"
tabulation= "yes"

#maps="yes"
maps="no"

#################################################################
# Run the reporting GFC loss and PFL loss by LFT and RC on admin units
################################################################# 

# Location of script 
reportScript = ("C:\\Data_Molinario\\Dropbox\\PhD\\Scripts\\arcpyReportRasters.py")
if "yes" in tabulation:
    print "python "+ reportScript
    handle = os.system("python "+reportScript)
    print "Version: "+version+". All report tables by units of area have been created."
else:
    print "Skipping run tabulation of results."

#################################################################
# Run automatic generation of maps and animated gifs
#################################################################

# Location of script 
createMapsGifsScript = ("C:\\Data_Molinario\\Dropbox\\PhD\\Scripts\\arcpyMappingLayerSwitch.py")

if "yes" in maps:
    print "python "+ createMapsGifsScript
    handle = os.system("python "+createMapsGifsScript)
    print "Version: "+version+". All map illustrations and animated gifs have been created."
else:
    print "Skipping run creation of maps and gifs."


#################################################################
# Run R to load tables, manipulate them, make figures
#################################################################

'''


# To do 


# End script 

