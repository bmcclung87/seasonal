import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import pickle
import os
import julian
import datetime
from datetime import timezone

dt = datetime.datetime(year=1948,month=1,day=1,hour=13,tzinfo=timezone.utc)
jd = julian.to_jd(dt, fmt='jd')

dir_bins = np.linspace(0,360,37)
speeds = np.linspace(0,40,9)
seasons = ['Summer','Fall','Winter','Spring']
pres_lvl = [925, 850, 700, 500]

for i in range(len(seasons)):
   filename = 'pickles/'+seasons[i]+'_OAK_soundings.p'
   data = pickle.load(open(filename,'rb'))
   cols = data.columns
   for j in range(len(pres_lvl)):
       for k in range(len(speeds)):
           dir_data = data.loc[ (data[cols[-3]]>=speeds[k]) & (data[cols[5]]>=pres_lvl[j]) & (data[cols[0]]>=1948),cols[-2]]
           dir_data = dir_data[~np.isnan(dir_data)]
           dir_hist,bins = np.histogram(dir_data,dir_bins)
           width = np.diff(dir_bins)
           center = (dir_bins[:-1]+dir_bins[1:])/2

           plt.figure()
           plt.bar(center,dir_hist,align='center',width=width)
           plt.xlabel('Wind Direction (deg)')
           plt.ylabel('Frequency')
           plt.title(seasons[i] + ', Years: 1948-2018, Wind Speed >= ' +str(int(speeds[k])) + ' kts, for Pressures >= '+str(int(pres_lvl[j]))+' mb')
           plt.savefig('images/OAK_'+seasons[i]+'_'+str(int(pres_lvl[j]))+'mb'+'_'+str(int(speeds[k]))+'kts')
           plt.close()

print('end of script')