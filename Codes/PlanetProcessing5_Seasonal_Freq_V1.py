#September 11 2023 - Victoria Hill (vhill@odu.edu)



#This code generates seasonal frequency rasters - you have to have run the intial calssifcaiton and freq code first
##1 _Search the SAV_presence folder
##2_ Make list of file names from Jan, Feb, MArch, April - May, June, July, August - Sept, Oct, Nov, Dec
##3_ Do same for Pixels__imaged folder
##4_ Generate seasonal freq rasters





#############import packages#############
import arcpy
import arcpy
from arcpy import env
from arcpy.sa import *
import os
import pandas as pd
import numpy as np
from tkinter import filedialog #for Python 3
import datetime
#########################################
arcpy.env.overwriteOutput = True

#######get working directory##################
topdir = filedialog.askdirectory(title='Select working directory')
print('Your working directory is: '+topdir)
##############################################
#######set input directory##################
fld_SAVpresence = '5a_SAV_presence'
path_SAVpresence = os.path.abspath(os.path.join(topdir, fld_SAVpresence)) 
# Creates the folder, and checks if it is created or not.
os.makedirs(path_SAVpresence, exist_ok=True)
##############################################
fld_imaged = '5b_pixels_imaged'
path_imaged = os.path.abspath(os.path.join(topdir, fld_imaged)) 
# Creates the folder, and checks if it is created or not.
os.makedirs(path_imaged, exist_ok=True)
##############################################
fld_freq = '5c_SAV_frequency'
path_freq = os.path.abspath(os.path.join(topdir, fld_freq)) 
# Creates the folder, and checks if it is created or not.
os.makedirs(path_freq, exist_ok=True)

#######################################################################################################
#######QUERY SAV PRESENCE FILES######################################################
#######################################################################################################
searchdirectory=path_SAVpresence
#Get all files in 5a_SAVpresence
listfiles_SAVpresence=[]
file_dates=[]#pd.DataFrame(columns=['date','season'])
for root, dirs, files in os.walk(searchdirectory):
    for filename in files:
        if filename.endswith(('_SAVpresence.tif')):
            #get first 8 characters which is the date
            imagedate=filename[0:8]
            #append date
            file_dates.append(imagedate)
            #append full file apth
            fullfile=os.path.abspath(os.path.join(path_SAVpresence,filename))
            listfiles_SAVpresence.append(fullfile)
            
#make file_dates into a dataframe            
df = pd.DataFrame(file_dates, columns=['date'])
#convert to datetime
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
#add fullpath of images to dataframe
df['fullpath']= listfiles_SAVpresence
#add numeric season
# % 12 is used to calculate the remainder when dividing the month values by 12. This is done to ensure that the result is between 0 and 11, as there are 12 months in a year.
# + 3 is added to the result from step 2. This is done to shift the month values by 3. For example, if the original month was January (1), it would become April (1 + 3 = 4), and if the original month was December (12), it would become March (12 + 3 = 15).
# // 2 is used to perform integer division by 2. This effectively maps the shifted month values to a range of 0 to 5. So, January to March maps to 0, April to June maps to 1, and so on, up to November to January mapping to 5.
#df['season'] = (df['date'].dt.month%12 + 3)//3
df['season'] = df['date'].dt.month
#add text season name
seasons = {1: 'Winter',2: 'Winter',3: 'Winter',4: 'Spring',5: 'Spring',6: 'Spring',7: 'Summer',8: 'Summer',9: 'Autumn', 10: 'Autumn', 11: 'Autumn', 12: 'other'}
#seasons = {1: 'Winter',2: 'Spring',3: 'Summer', 4: 'Autumn'}
#map season name to dataframe
df['season_name'] = df['season'].map(seasons)

#select images from the spring
spring_images=df[df.season_name == 'Spring']
spring_list = spring_images['fullpath'].tolist()
spring_count=len(spring_list)

summer_images=df[df.season_name == 'Summer']
summer_list = summer_images['fullpath'].tolist()
summer_count=len(summer_list)

autumn_images=df[df.season_name == 'Autumn']
autumn_list = autumn_images['fullpath'].tolist()
autumn_count=len(autumn_list)

winter_images=df[df.season_name == 'Winter']
winter_list = winter_images['fullpath'].tolist()
winter_count=len(winter_list)


#######################################################################################################
#######QUERY PIXELS IAMGED FILES######################################################
#######################################################################################################
searchdirectory=path_imaged
#Get all files in 5a_SAVpresence
listfiles_imaged=[]
imaged_dates=[]#pd.DataFrame(columns=['date','season'])
for root, dirs, files in os.walk(searchdirectory):
    for filename in files:
        if filename.endswith(('_imaged.tif')):
            #get first 8 characters which is the date
            imagedate=filename[0:8]
            #append date
            imaged_dates.append(imagedate)
            #append full file apth
            fullfile=os.path.abspath(os.path.join(path_imaged,filename))
            listfiles_imaged.append(fullfile)
            
#make file_dates into a dataframe            
df_imaged = pd.DataFrame(imaged_dates, columns=['date'])
#convert to datetime
df_imaged['date'] = pd.to_datetime(df_imaged['date'], format='%Y%m%d')
#add fullpath of images to dataframe
df_imaged['fullpath']= listfiles_imaged
#add numeric season
# % 12 is used to calculate the remainder when dividing the month values by 12. This is done to ensure that the result is between 0 and 11, as there are 12 months in a year.
# + 3 is added to the result from step 2. This is done to shift the month values by 3. For example, if the original month was January (1), it would become April (1 + 3 = 4), and if the original month was December (12), it would become March (12 + 3 = 15).
# // 2 is used to perform integer division by 2. This effectively maps the shifted month values to a range of 0 to 5. So, January to March maps to 0, April to June maps to 1, and so on, up to November to January mapping to 5.
#df_imaged['season'] = (df_imaged['date'].dt.month%12 + 3)//3
df_imaged['season'] = df_imaged['date'].dt.month
#add text season name
#seasons = {1: 'Winter',2: 'Winter',3: 'Winter',4: 'Spring',5: 'Spring',6: 'Spring',7: 'Summer',8: 'Summer',9: 'Autumn', 10: 'Autumn', 11: 'Autumn', 12: 'other'}
#add text season name
#seasons = {1: 'Winter',2: 'Spring',3: 'Summer', 4: 'Autumn'}
#map season name to dataframe
df_imaged['season_name'] = df_imaged['season'].map(seasons)

#select images from the spring
spring_images=df_imaged[df_imaged.season_name == 'Spring']
spring_list_imaged = spring_images['fullpath'].tolist()

summer_images=df_imaged[df_imaged.season_name == 'Summer']
summer_list_imaged = summer_images['fullpath'].tolist()

autumn_images=df_imaged[df_imaged.season_name == 'Autumn']
autumn_list_imaged = autumn_images['fullpath'].tolist()


winter_images=df_imaged[df_imaged.season_name == 'Winter']
winter_list_imaged = winter_images['fullpath'].tolist()

##
#######################################################################################################
#######SPRING#####################################################
#######################################################################################################
if spring_count == 0:
    print('No spring files')
else:
    print('I found '+str(len(spring_list))+' spring files to process')
    print('***************************')
    season='Spring'
    path_site=os.path.basename(topdir)
    presencename=path_site+'_'+season+'_SAVpresence.tif'
    imagedname=path_site+'_'+season+'_imaged.tif'
    percentname=path_site+'_'+season+'_percentSAV.tif'
    
    with arcpy.EnvManager(extent="MAXOF"):
        spring_virtual = [arcpy.Raster(i) for i in spring_list]
        presencename_out= os.sep.join([path_freq, presencename])
        outSAVpresence = CellStatistics(spring_virtual, "SUM", "", "") #you are summing all overlapping pixels, so SAV has to equal 1 in all your mosaiced files
        outSAVpresence.save(presencename_out)#change this to save your frequency file
    with arcpy.EnvManager(extent="MAXOF"):
        spring_virtual = [arcpy.Raster(i) for i in spring_list_imaged]
        imagedname_out= os.sep.join([path_freq, imagedname])
        outimaged = CellStatistics(spring_virtual, "SUM", "", "") #you are summing all overlapping pixels, so SAV has to equal 1 in all your mosaiced files
        outimaged.save(imagedname_out)#change this to save your frequency file       
    print('Calculating % SAV presence')

    percentfilename_location= os.sep.join([path_freq, percentname])

    precentSAV=(Raster(outSAVpresence)/Raster(outimaged))*100
    precentSAV.save(percentfilename_location)
    print('Spring finished')

#######################################################################################################
#######SUMMER######################################################
#######################################################################################################
if summer_count == 0:
    print('No summer files')
else:
    print('I found '+str(len(summer_list))+' summer files to process')
    print('***************************')
    season='Summer'
    path_site=os.path.basename(topdir)
    presencename=path_site+'_'+season+'_SAVpresence.tif'
    imagedname=path_site+'_'+season+'_imaged.tif'
    percentname=path_site+'_'+season+'_percentSAV.tif'
   
    with arcpy.EnvManager(extent="MAXOF"):
        summer_virtual = [arcpy.Raster(i) for i in summer_list]
        presencename_out= os.sep.join([path_freq, presencename])
        outSAVpresence = CellStatistics(summer_virtual, "SUM", "", "") #you are summing all overlapping pixels, so SAV has to equal 1 in all your mosaiced files
        outSAVpresence.save(presencename_out)#change this to save your frequency file
    with arcpy.EnvManager(extent="MAXOF"):
        summer_virtual = [arcpy.Raster(i) for i in summer_list_imaged]
        imagedname_out= os.sep.join([path_freq, imagedname])
        outimaged = CellStatistics(summer_virtual, "SUM", "", "") #you are summing all overlapping pixels, so SAV has to equal 1 in all your mosaiced files
        outimaged.save(imagedname_out)#change this to save your frequency file       
    print('Calculating % SAV presence')

    percentfilename_location= os.sep.join([path_freq, percentname])

    precentSAV=(Raster(outSAVpresence)/Raster(outimaged))*100
    precentSAV.save(percentfilename_location)
    print('Summer finished')
##    
#######################################################################################################
#######AUTUMN###################################################
#######################################################################################################
if autumn_count == 0:
    print('No Autumn files')
else:
    print('I found '+str(len(autumn_list))+' Autumn files to process')
    print('***************************')
    season='Autumn'
    path_site=os.path.basename(topdir)
    presencename=path_site+'_'+season+'_SAVpresence.tif'
    imagedname=path_site+'_'+season+'_imaged.tif'
    percentname=path_site+'_'+season+'_percentSAV.tif'
   
    with arcpy.EnvManager(extent="MAXOF"):
        autumn_virtual = [arcpy.Raster(i) for i in autumn_list]
        presencename_out= os.sep.join([path_freq, presencename])
        outSAVpresence = CellStatistics(autumn_virtual, "SUM", "", "") #you are summing all overlapping pixels, so SAV has to equal 1 in all your mosaiced files
        outSAVpresence.save(presencename_out)#change this to save your frequency file
    with arcpy.EnvManager(extent="MAXOF"):
        autumn_virtual = [arcpy.Raster(i) for i in autumn_list_imaged]
        imagedname_out= os.sep.join([path_freq, imagedname])
        outimaged = CellStatistics(autumn_virtual, "SUM", "", "") #you are summing all overlapping pixels, so SAV has to equal 1 in all your mosaiced files
        outimaged.save(imagedname_out)#change this to save your frequency file       
    print('Calculating % SAV presence')

    percentfilename_location= os.sep.join([path_freq, percentname])

    precentSAV=(Raster(outSAVpresence)/Raster(outimaged))*100
    precentSAV.save(percentfilename_location)
    print('Autumn finished')

#######################################################################################################
#######WINTER###################################################
#######################################################################################################
if winter_count == 0:
    print('No Winter files')
else:
    print('I found '+str(len(winter_list))+' winter files to process')
    print('***************************')
    season='winter'
    path_site=os.path.basename(topdir)
    presencename=path_site+'_'+season+'_SAVpresence.tif'
    imagedname=path_site+'_'+season+'_imaged.tif'
    percentname=path_site+'_'+season+'_percentSAV.tif'
   
    with arcpy.EnvManager(extent="MAXOF"):
        winter_virtual = [arcpy.Raster(i) for i in winter_list]
        presencename_out= os.sep.join([path_freq, presencename])
        outSAVpresence = CellStatistics(winter_virtual, "SUM", "", "") #you are summing all overlapping pixels, so SAV has to equal 1 in all your mosaiced files
        outSAVpresence.save(presencename_out)#change this to save your frequency file
    with arcpy.EnvManager(extent="MAXOF"):
        winter_virtual = [arcpy.Raster(i) for i in winter_list_imaged]
        imagedname_out= os.sep.join([path_freq, imagedname])
        outimaged = CellStatistics(winter_virtual, "SUM", "", "") #you are summing all overlapping pixels, so SAV has to equal 1 in all your mosaiced files
        outimaged.save(imagedname_out)#change this to save your frequency file       
    print('Calculating % SAV presence')

    percentfilename_location= os.sep.join([path_freq, percentname])

    precentSAV=(Raster(outSAVpresence)/Raster(outimaged))*100
    precentSAV.save(percentfilename_location)
    print('Winter finished')    
