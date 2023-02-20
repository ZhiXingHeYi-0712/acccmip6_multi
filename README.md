### About this project
This project is used for downloading CMIP6 by multi-thread, modified from https://github.com/TaufiqHassan/acccmip6.

### Usage

Everything but multi-thread download is the same as the source project, just refer https://github.com/TaufiqHassan/acccmip6 for more details.

If you want to enable multi-thread download, please use `-multi` and `-workers`.

Here is an example:
```
acccmip6 -o D -v pr -f mon -e historical,ssp126,ssp245,ssp370,ssp585 -m BCC-CSM2-MR -multi True -workers 8
```

if you want to stop using multi-thread, just
```
acccmip6 -o D -v pr -f mon -e historical,ssp126,ssp245,ssp370,ssp585 -m BCC-CSM2-MR -multi False
```
or just ignore them, like
```
acccmip6 -o D -v pr -f mon -e historical,ssp126,ssp245,ssp370,ssp585 -m BCC-CSM2-MR
```

The multi-thread will not affect the search or the download of CMIP6DB module.

### Known bugs
The download progress bar will work incorrectly when using the multi-thread download.

Actually, for it has no more consequence, I'm not very much care about it, so I probably won't fix it. 
