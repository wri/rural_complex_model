
####################################################################
# This script builds the input mask for the LFT
#
#	- V14 modeled the final version for the 2015 paper
# 		GM 06/25/2014
# 		revision for v14
#			10/30/2014
#			11/09/2014
#
#	- Previously the mask was built manually and then refined with script arcpyBuildSelectionMaskForNFandWD.py
#
# 	- v15 - 07/14/2016 - This version adds GFC loss to the v14 modelled 2000 input mask
# 	- v17 at 30m res but the same time periods 
#	- v18 at 30m and YEARLY lft folders? 
#
#
#
# 08/16/2016 need to fix so  that master masks for 2005,2010 and 2014 have the NON forest classed 
# as a zero and not NoData  - seems like the LFT worked well anyway, but the master files were 
# incorrect and I fixed them manually. 
####################################################################


####################################################################
#Import arcpy modules
import arcpy
from arcpy import env
from arcpy.sa import *
import os

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

####################################################################
# Global variables and folders

maskVersion= 'V17'
# LFT directory
root=r"C:\Data_Molinario\temp\LFT_local\17th_run"

# 2000 Master mask 
MaskFolder2000=r"\2000\Master"

# Path to 2000 Master mask
MaskFolder2000Path=root+"/"+MaskFolder2000

#Old working version of product is v14
oldVersion=r"C:\Data_Molinario\temp\LFT_local\17th_run"

#Old version path
oldVersionPath=oldVersion+"/"+MaskFolder2000


# Snap raster variable
tempEnvironment0 = arcpy.env.snapRaster
arcpy.env.snapRaster = r"Z:\Giuseppe\PhD\FACET_DRC\FACET_DRC_original\map.tif"

# Set extent variable
arcpy.env.extent = r"Z:\Giuseppe\PhD\FACET_DRC\FACET_DRC_original\map.tif"

# Overwrite existing raster variable 
arcpy.env.overwriteOutput=True

# yearly LFT version:
# First period
# base=2000
# Periods of LFT 
# LFTs= ["2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2014"]
LFTs=["2005","2010","2014"]

###############################################################################


####################################################################
# Build root folder structure to put final Master LFT input masks in
####################################################################

# Master folder
lftMaster = "Master"
for lft in LFTs:
	# Make the period folder
	outputFolder=str(lft)
	# Period folder path
	outputFolderPath = root+"/"+outputFolder
	# Create the folder if it doesn't exist
	if not os.path.exists(outputFolderPath):
		os.makedirs(outputFolderPath)
		print "Made "+str(lft)+" folder."
	# Create the master folder in it
	masterFolderPath=outputFolderPath+"/"+lftMaster
	if not os.path.exists(masterFolderPath):
		os.makedirs(masterFolderPath)
		print "Made Master folder for "+str(lft)+"."

###############################################################################	
# Copy 2000 Master mask from the old working version (v14) into the new version
###############################################################################

# Comment if already copied. 
'''
env.workspace=oldVersionPath
raster=arcpy.ListRasters("*final*")[0]
destination=MaskFolder2000Path+"/"+raster
print raster
arcpy.CopyRaster_management(raster,destination,"DEFAULTS","","","","","")
'''

########################################################
# Readme - Manually copy folders that are not automated: 
########################################################

# - Check the following below:
	# - Raw_input_mask (unless I build it with script) ? 
	# - Core_stratification folder
	# - Rural_complex folder
	# - WaterAndNoData folder
	# - AOI folder


###############################################
# Readme - process to build LFT input mask
###############################################
#
# - Input masks in previous version are built by: arcpyBuildInputMaskForLFT_v2.py
# 		- arcpyBuildInputMaskForLFT_v2.py does the modelling of 2000 classes to separate "anthropogenic" NF, WD and SF, 
# - v16 script - 07/2016 update -  use GFC loss, not FACET in 2005, 2010, 2014  to add GFC loss to mask created in 2000. 
# - v17 does that at 30m

		# For 2000 include:
		#		Class 0: All water and NoData, all large NF and WD not close to FACET loss. 
		#		Class 1: 
		#			- SF only if large groups or small groups if in proximity of PFL or SFL 2005/2010
		#				- Filtered for MMU, no single pixels
		#			- NF and WD only small groups if in proximity of PFL or SFL 2005/2010
		#				- Filtered for MMU, no single pixels go to NoData 
		#		Class 2: All PF
		#
		# For all other years:
		#		Class 0: All water and NoData, all large NF and WD not close to loss. 
		#		Class 1: 
		#				- As above, then add also:
		#				- GFC loss for that year
		#		Class 2: All PF
		#

######################################################
# Reclassify the total GFC raster into period rasters
######################################################

#gfc version 
gfcVersion = "v6"

# Input GFC raster already mosaiced and clipped to DRC extent
gfcRaster="Hansen_GFC2014_lossyear_Mosaic_DRC_sin_v6.tif"
print gfcRaster

# Input Path to the raster
gfcRasterPath=r"Z:\Giuseppe\PhD\GFC\GFC_2000_2014\LossYear\Mosaic\DRC"
print gfcRasterPath

# Set workspace to the GFC input path
env.workspace=gfcRasterPath
print env.workspace

# Select the GFC input raster
raster=arcpy.ListRasters("*"+gfcVersion+"*")[0]
print raster

# Output Path to the separated period masks
gfcPeriodPath=r"Z:\Giuseppe\PhD\GFC\GFC_2000_2014\LossYear\Mosaic\DRC\GFC_loss\GFC_Yearly_Masks"
print gfcPeriodPath


# Reclassify field of the .tif for the arcpy reclassify function
reclassField = "Value"

# 		Values
# 		0 - total
# 		1-4 = 2005
# 		5-9 = 2010
# 		10-14 = 2014
'''

for period in LFTs: 
	if "2005" in period:
		# Variable with the RemapRange table for reclassify
		remap=RemapRange([
	 	[0,0,0], # other loss
		[1,4,10], # loss years 1-4
		[5,14,0]])
		print remap
		# New name for the reclassified output
		name=gfcRaster[:-4]+"_"+period+".tif"
		print name
		# Path and name for the reclassified output
		namePath=gfcPeriodPath+"\\0_4\\"+name
		print name

	elif "2010" in period:
		# Variable with the RemapRange table for reclassify
		remap=RemapRange([
	 	[0,0,0], # other loss
		[1,9,10], # loss years 5-9
		[10,14,0]])
		print remap
		# New name for the reclassified output
		name=gfcRaster[:-4]+"_"+period+".tif"
		print name
		# Path and name for the reclassified output
		namePath=gfcPeriodPath+"\\5_9\\"+name
		print name

	elif "2014" in period:
		# Variable with the RemapRange table for reclassify
		remap=RemapRange([
	 	[0,0,0], # other loss
		[1,14,10]]) # final raster doesnt have 0 value because there is no input value that goes to 0. 
		print remap
		# New name for the reclassified output
		name=gfcRaster[:-4]+"_"+period+".tif"
		print name
		# Path and name for the reclassified output
		namePath=gfcPeriodPath+"\\10_14\\"+name
		print name
	else:
		pass


	# Reclassify and save based on the above remap
	outReclassify = Reclassify(raster, reclassField, remap)
	outReclassify.save(namePath)
	print "Separated GFC into period "+ period + " binary rasters."


	# Use condition to set NoData to 0 value
	arcpy.env.overwriteOutput=True
	outName=namePath[:-4]+"_noNullTemp.tif"
	conditional=Con(IsNull(namePath),0,namePath)
	conditional.save(outName)
	# Rewrite the output forcing it to 8 bit unsigned. 
	nullRaster=outName
	nullRasterFinal=outName[:-8]+".tif"
	##		Usage: CopyRaster_management(
	##			in_raster, out_rasterdataset, {config_keyword}, {background_value}, 
	##			{nodata_value}, {NONE | OneBitTo8Bit}, {NONE | ColormapToRGB}, 
	##			{1_BIT | 2_BIT | 4_BIT | 8_BIT_UNSIGNED | 8_BIT_SIGNED | 16_BIT_UNSIGNED | 
	##			16_BIT_SIGNED | 32_BIT_UNSIGNED | 32_BIT_SIGNED | 32_BIT_FLOAT | 64_BIT}, 
	##			{NONE | ScalePixelValue}, {NONE | RGBToColormap}, {TIFF | IMAGINE Image | 
	##			BMP | GIF | PNG | JPEG | JPEG2000 | Esri Grid | Esri BIL | Esri BSQ | 
	##			Esri BIP | ENVI | CRF | MRF}, {NONE | Transform})
	arcpy.CopyRaster_management(nullRaster,nullRasterFinal,"DEFAULTS","","","","","8_BIT_UNSIGNED")

	print "Rewrote GFC "+ period + " binary rasters so that NODATA is 0."

'''
##########################################################
# Merge the GFC binary period masks to the 2000 mask
##########################################################

# Get the 2000 base mask
env.workspace=MaskFolder2000Path
mask2000=raster=arcpy.ListRasters("*30m*")[0]
print mask2000

# List of the folders
periodFolders=["0_4","5_9","10_14"]
'''

for LFT in LFTs:
	print LFTs
	print "processing LFT: "+ LFT
	if "2005" in LFT:
		print LFT
		# Name for the period raster
		name=gfcRaster[:-4]+"_"+LFT+"_noNull.tif"
		print name
		# Path and name for the reclassified output
		periodRaster=gfcPeriodPath+"\\"+periodFolders[0]+"\\"+name
		# Create a merged raster
		merged = Raster(mask2000)+Raster(periodRaster)
		# Save the merged raster
		mergedOutputTemp=gfcPeriodPath+"\\"+periodFolders[0]+"\\"+name[:-4]+"_tmp_mrg.tif"
		mergedOutput=gfcPeriodPath+"\\"+periodFolders[0]+"\\"+name[:-4]+"_merged_30m.tif"
		print mergedOutput
		merged.save(mergedOutputTemp)
		arcpy.CopyRaster_management(mergedOutputTemp,mergedOutput,"DEFAULTS","","","","","8_BIT_UNSIGNED")
		print "Saved merged raster to "+ mergedOutput
	elif "2010" in LFT:
		print LFT
		# Name for the period raster
		name=gfcRaster[:-4]+"_"+LFT+"_noNull.tif"
		print name
		# Path and name for the reclassified output
		periodRaster=gfcPeriodPath+"\\"+periodFolders[1]+"\\"+name
		# Create a merged raster
		merged = Raster(mask2000)+Raster(periodRaster)
		# Save the merged raster
		mergedOutputTemp=gfcPeriodPath+"\\"+periodFolders[1]+"\\"+name[:-4]+"_tmp_mrg.tif"
		mergedOutput=gfcPeriodPath+"\\"+periodFolders[1]+"\\"+name[:-4]+"_merged_30m.tif"
		print mergedOutput
		merged.save(mergedOutputTemp)
		arcpy.CopyRaster_management(mergedOutputTemp,mergedOutput,"DEFAULTS","","","","","8_BIT_UNSIGNED")
		print "Saved merged raster to "+ mergedOutput
	elif "2014" in LFT:
		print LFT
		# Name for the period raster
		name=gfcRaster[:-4]+"_"+LFT+"_noNull.tif"
		print name
		# Path and name for the reclassified output
		periodRaster=gfcPeriodPath+"\\"+periodFolders[2]+"\\"+name
		# Create a merged raster
		merged = Raster(mask2000)+Raster(periodRaster)
		# Save the merged raster
		mergedOutputTemp=gfcPeriodPath+"\\"+periodFolders[2]+"\\"+name[:-4]+"_tmp_mrg.tif"
		mergedOutput=gfcPeriodPath+"\\"+periodFolders[2]+"\\"+name[:-4]+"_merged_30m.tif"
		print mergedOutput
		merged.save(mergedOutputTemp)
		arcpy.CopyRaster_management(mergedOutputTemp,mergedOutput,"DEFAULTS","","","","","8_BIT_UNSIGNED")
		print "Saved merged raster to "+ mergedOutput

'''

#############################################################################################
# Reclassify and save the merged raster
# - then copy it into Temp LFT folder
#############################################################################################

for LFT in LFTs: 
	print LFTs
	print "processing LFT: "+ LFT
	if "2005" in LFT:
		print LFT
		remap=RemapValue([
			[0,0], # stays all not land or not disturbd
			[1,1], # stays all disturbed
			[2,2], # stays all primary forest
			[10,0], #GFC loss in mask 2000 not disturbable - stays as 0
			[11,1], #GFC loss in mask 2000 disturbed, stays disturbed as 1
			[12,1]]) #GFC loss in mask 2000 primary forest, becomes disturbed as 1 in new period
		print remap
		# New name for the reclassified output
		nameMaster=mask2000[:-18]+LFT+"_final.tif"
		print nameMaster
		# Path and name for the reclassified output
		namePath=root+"\\"+LFT+"\\Master\\"+nameMaster
		print namePath
		nameMerged=gfcRaster[:-4]+"_"+LFT+"_noNull_merged_30m.tif"
		mergedOutput=gfcPeriodPath+"\\"+periodFolders[0]+"\\"+nameMerged
	elif "2010" in LFT:
		remap=RemapValue([
			[0,0], # stays all not land or not disturbd
			[1,1], # stays all disturbed
			[2,2], # stays all primary forest
			[10,0], #GFC loss in mask 2000 not disturbable - stays as 0
			[11,1], #GFC loss in mask 2000 disturbed, stays disturbed as 1
			[12,1]]) #GFC loss in mask 2000 primary forest, becomes disturbed as 1 in new period
		print remap
		# New name for the reclassified output
		nameMaster=mask2000[:-18]+LFT+"_final.tif"
		print nameMaster
		# Path and name for the reclassified output
		namePath=root+"\\"+LFT+"\\Master\\"+nameMaster
		print namePath
		nameMerged=gfcRaster[:-4]+"_"+LFT+"_noNull_merged_30m.tif"
		mergedOutput=gfcPeriodPath+"\\"+periodFolders[1]+"\\"+nameMerged
	elif "2014" in LFT:
		remap=RemapValue([
			[0,0], # stays all not land or not disturbd
			[1,1], # stays all disturbed
			[2,2], # stays all primary forest
			[10,0], #GFC loss in mask 2000 not disturbable - stays as 0
			[11,1], #GFC loss in mask 2000 disturbed, stays disturbed as 1
			[12,1]]) #GFC loss in mask 2000 primary forest, becomes disturbed as 1 in new period
		print remap
		# New name for the reclassified output
		nameMaster=mask2000[:-18]+LFT+"_final.tif"
		print nameMaster
		# Path and name for the reclassified output
		namePath=root+"\\"+LFT+"\\Master\\"+nameMaster
		print namePath
		nameMerged=gfcRaster[:-4]+"_"+LFT+"_noNull_merged_30m.tif"
		mergedOutput=gfcPeriodPath+"\\"+periodFolders[2]+"\\"+nameMerged
	else:
		pass

	outRaster= mergedOutput[:-14]+"rcl.tif"

	# Reclassify the merged rasters for each period	
	outReclassify = Reclassify(mergedOutput, reclassField, remap)
	# Save the reclassified merged raster
	outReclassify.save(outRaster)
	print "Saved the final reclassified raster as: " + namePath

	# Copy the raster into the temp\LFT folder to run the LFT
	# arcpy.CopyRaster_management(outRaster,namePath,"DEFAULTS","","","","","")
	arcpy.CopyRaster_management(outRaster,namePath,"DEFAULTS","","","","","8_BIT_UNSIGNED")
	print "Added period "+ LFT+ " GFC to mask 2000, reclassified and copied to "+ LFT+ " Master folder."


# print "Mask for "+ period + " exported. Version "+maskVersion


# Next run the LFT script.




