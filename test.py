from acccmip6.download_dat import DownloadCmip6
import os
os.chdir('D:/Code/CMIP_downscaling/BCC_historical/')

DownloadCmip6(model='BCC-CSM2-MR', experiment='historical', variable='co2', frequency='mon', path='other_data', rlzn='1', multi=True, workers=4, year=-15)
