
# coding: utf-8

# # Fetch and plot ECMWF MSL Pressure

# **Creator:** Leo Peach
# 
# **Purpose:** To download and create animated plots of the ECMWF pressure data available from the FTP
# 
# **Date:** 08/02/2019
# 
# **TODO:** Currently there is a need to save the grib file as a local tempfile, as well as an index temp file which wraps the grib file into a usable object, this is not ideal, eventually this will all work in memory

# In[53]:


from ftplib import FTP
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap
import os
import io
import numpy as np
from PIL import Image


# In order the grab the data we need to ensure that we are getting it through the departmental ftp proxy server

# In[54]:


def download_ftp():
    """Downloads data from the ftp server (currently seupt to go through departmental proxy)
    Returns list fo xr datasets"""

    #ftp proxy required for work
    #site = FTP("gw-ftp.dmz")
    #msg = site.login('wmo@dissemination.ecmwf.int', 'essential')
    #for without proxy below
    site = FTP("dissemination.ecmwf.int")
    msg = site.login('wmo', 'essential')
    
    #get a list of the folders
    files = []

    try:
        files = site.nlst()
    except ftplib.error_perm:
        if str(resp) == "550 No files found":
            print("No files in this directory")
        else:
            raise

    #change directory to the latest model runs
    site.cwd("/"+files[-1])
    
    #now list the files in that directory
    files = []

    try:
        files = site.nlst()
    except ftplib.error_perm:
        if str(resp) == "550 No files found":
            print("No files in this directory")
        else:
            raise
    
    #grab MSL pressure Grib file names
    msl_files = []
    for file in files:
        if 'msl' in file:
            if 'em' in file:
                continue
            if 'es' in file:
                continue
            msl_files.append(file)
            
    
    # make temp files and make each one an xarray, then add to list
    
    xarrays = []
    
    filename = 'mytempgrib_'
    x = 0
    for run in msl_files[0:5]:
        newfilename =  filename+str(x)+'.grib'
        localfile = open(newfilename, 'wb')
        x +=1
        try:
            site.retrbinary('RETR ' + run, localfile.write, 1024)
        except:
            print("Error")
        localfile.close()
        
        ds = xr.open_dataset(os.getcwd()+'/'+newfilename, engine='cfgrib')
        xarrays.append(ds)
    site.close()
    return xarrays
    


# In[70]:


def make_plot(xarrays):
    """takes in a list of xarrays and returns a gif animation"""
    
    import matplotlib.cm as cm
    from mpl_toolkits.basemap import Basemap
    import numpy as np


    pres_max = 1010.0
    pres_min = 990.0
    fig, axes = plt.subplots(figsize=(10,8))

    #Coords for centre of Australia
    lon_0 = 134 
    lat_0 = -23
    
    maps = []
    
    time = xarrays[0].time.data    
    
    for ds in xarrays:
        # tries to keeps the max and min ranges the same (needs work)
        if (ds.msl.values /100).max() > pres_max:
                pres_max = (ds.msl.values /100).max()
        if (ds.msl.values /100).min() < pres_max:    
                pres_min = (ds.msl.values /100).min()
    
        #build map object
        map_ax = Basemap(resolution='l',projection='tmerc', lat_0=lat_0,lon_0=lon_0, llcrnrlon=100, llcrnrlat=-42
                   ,urcrnrlon=160, urcrnrlat=-8.0)
        lon, lat = np.meshgrid(ds.longitude.data, ds.latitude.data)
        xi, yi = map_ax(lon, lat)
        map_ax.contour(xi, yi, (ds.msl.values /100), 10, vmin = pres_min, vmax = pres_max, colors="black")
        im = map_ax.contourf(xi, yi,(ds.msl.values/100), 10, vmin = pres_min, vmax = pres_max, cmap=plt.get_cmap("jet"))
        m = plt.cm.ScalarMappable(cmap=cm.coolwarm)
        m.set_array((ds.msl.values /100))
        m.set_clim(pres_min, pres_max)
        
        # Add a color bar
        cbar = plt.colorbar(im, boundaries=np.arange(pres_min,pres_max,4))
        cbar.set_label('Sea Level Pressure (hPa)')

        map_ax.drawcoastlines()
        map_ax.drawstates()
        
        # timestamp for data
        plt.title(str(time)[:-5])
        time = time + np.timedelta64(24, 'h')
        
        #save as memobj
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        maps.append(Image.open(buf))
        
        #clear plot
        plt.clf()
        
    #generate gif animation
    gif = io.BytesIO()
    maps[0].save(gif, format = 'gif', save_all=True, append_images=maps[1:], duration =1000, loop=0)
    gif.seek(0)
    import base64
    data_uri = base64.b64encode(gif.read()).decode('ascii')
    return data_uri


# In[95]:


def make_plot_QLD(xarrays):
    """takes in a list of xarrays and returns a gif animation"""
    
    import matplotlib.cm as cm
    from mpl_toolkits.basemap import Basemap
    import numpy as np


    pres_max = 1010.0
    pres_min = 990.0
    fig, axes = plt.subplots(figsize=(10,8))

    #Coords for centre of Australia
    lon_0 = 134 
    lat_0 = -23
    
    maps = []
    
    time = xarrays[0].time.data    
    
    for ds in xarrays:
        # tries to keeps the max and min ranges the same (needs work)
        if (ds.msl.values /100).max() > pres_max:
                pres_max = (ds.msl.values /100).max()
        if (ds.msl.values /100).min() < pres_max:    
                pres_min = (ds.msl.values /100).min()
    
        #build map object
        map_ax = Basemap(resolution='l',projection='tmerc', lat_0=lat_0,lon_0=lon_0, llcrnrlon=130, llcrnrlat=-30
                   ,urcrnrlon=160, urcrnrlat=-8.0)
        lon, lat = np.meshgrid(ds.longitude.data, ds.latitude.data)
        xi, yi = map_ax(lon, lat)
        map_ax.contour(xi, yi, (ds.msl.values /100), 10, vmin = pres_min, vmax = pres_max, colors="black")
        im = map_ax.contourf(xi, yi,(ds.msl.values/100), 10, vmin = pres_min, vmax = pres_max, cmap=plt.get_cmap("jet"))
        m = plt.cm.ScalarMappable(cmap=cm.coolwarm)
        m.set_array((ds.msl.values /100))
        m.set_clim(pres_min, pres_max)
        
        # Add a color bar
        cbar = plt.colorbar(im, boundaries=np.arange(pres_min,pres_max,4))
        cbar.set_label('Sea Level Pressure (hPa)')

        map_ax.drawcoastlines()
        map_ax.drawstates()
        
        # timestamp for data
        plt.title(str(time)[:-5])
        time = time + np.timedelta64(24, 'h')
        
        #save as memobj
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        maps.append(Image.open(buf))
        
        #clear plot
        plt.clf()
        
    #generate gif animation
    gif = io.BytesIO()
    maps[0].save(gif, format = 'gif', save_all=True, append_images=maps[1:], duration =1000, loop=0)
    gif.seek(0)
    import base64
    data_uri = base64.b64encode(gif.read()).decode('ascii')
    return data_uri


# In[96]:


def cleanup():
    """deletes all the temporary files we have created"""
    files_List = []
    print('cleaning up temp files')
    for (dirname, dirs, files) in os.walk('.'):
        for filename in files:
            if "mytempgrib_" in filename :
                #files_List.append(os.path.join(os.getcwd(), filename))
                os.remove(os.path.join(os.getcwd(), filename))
    return files_List


# In[97]:


def main():
    
    model_data = download_ftp()
    print('Building file')
    name = '/home/leo/Python/web_projects/DrakonianMight.github.io/Pressure/index.html'
    html = open(name, 'w')
    html.write("<head><title>Forecast Data Loops</title></head>\n")
    html.write("<h1>Forecast Data Loops</h1>\n")
    html.write("<p>Forecasting loops from the ECMWF model showing mean sea level pressure &copy; ECMWF</p>\n")
    html.write("<br></br><body>")
    html.write("<h3>Australia 4 day forecast</h3>\n")
    html.write('<img src="data:image/png;base64,{0}">'.format(make_plot(model_data)))
    html.write("<br></br>\n")
    html.write("<h3>Queensland 4 day forecast</h3>\n")
    html.write('<img src="data:image/png;base64,{0}">'.format(make_plot_QLD(model_data)))
    html.write("</body>")
    html.close()
    print('complete')
    cleanup()
    return


# In[98]:


main()

