# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 21:05:20 2019

@author: Taufiq
"""
from __future__ import unicode_literals
from concurrent.futures import ThreadPoolExecutor, wait
import urllib.request
import os, sys
import time
import numpy as np
from pathlib import Path

from acccmip6.utilities.util import color, _dir_path, TooSlowException, convertBToMb, _realizations
from acccmip6.utilities.util import _get_rlzn_links, _manual_wget, HidePrint, _get_skipped_links
from acccmip6.utilities.c6db import SearchDB


def getTimeRange(start_year, end_year, year_list):
    year_list = [int(y) for y in year_list]
    year_list.sort()
    year_list = np.array(year_list)

    if np.all(start_year < year_list):
        # too early
        raise Exception('Start Time is too early!')
    
    if np.all(start_year > year_list):
        return [year_list[-1]]
    if np.all(end_year > year_list):
        end_index = len(year_list) + 100
    else:
        end_index   = np.nonzero((end_year - year_list) < 0)[0][0]

    start_index = np.nonzero((year_list - start_year) <= 0)[0][-1]

    return list(year_list[start_index:end_index])


def dlControl(count, blockSize, totalSize):
    global startTime

    dLoaded = count*blockSize
    passedTime = time.time() - startTime
    tRate = convertBToMb(dLoaded) / passedTime
    csize = int(convertBToMb(dLoaded))
    tsize = int(convertBToMb(totalSize))

    barLength = 40
    progress = float(csize) / float(tsize)
    percent = (csize/tsize)*100
    block = int(round(barLength * progress))
    text2="\r%s %i%% |%s%s| %i/%iMB %.2f MB/s\r" % ("Downloading ", percent, "█"*block, "░"*(barLength-block), csize, tsize, tRate)
    sys.stdout.write(text2)
    sys.stdout.flush()

    if (tRate < 0.08) and (passedTime > 60):
        print ("\ndownload too slow! retrying...")
        time.sleep(2)
        raise TooSlowException

def dl_cmip6(durl, dir_path):
        
        if (not os.path.exists(durl.split('/')[len(durl.split('/'))-1])):
            print("\n\n"+durl.split('/')[len(durl.split('/'))-1]+" is available!\n")
            urllib.request.urlretrieve(durl,durl.split('/')[len(durl.split('/'))-1],reporthook=dlControl)
        else:
            print("\n"+durl.split('/')[len(durl.split('/'))-1]+" already exists!\n")         


def single_download(params):
    global startTime
    
    url, dir_path, passed_urls, download_record = params
    startTime = time.time()
    try:
        dl_cmip6(url, dir_path)
        download_record['n']=download_record['n']+1
        passed_urls.append(url)
    except TooSlowException:
        print("Removing file . . .\n")
        os.remove(url.split('/')[len(url.split('/'))-1])
        download_record['m']=download_record['m']+1
        startTime = time.time()
    except KeyboardInterrupt:
        print("\nInterrupted! Removing file . . .\n")
        os.remove(url.split('/')[len(url.split('/'))-1])
        return
    except urllib.error.HTTPError:
        download_record['m']=download_record['m']+1
        download_record['manual']=download_record['manual']+1
        print("\n"+color.RED+"<<401 Unauthorized: restricted access!!>>"+color.END+"\n")
        print(color.UNDERLINE+"From ESGF:"+color.END+" Before you can download this data, you have to join a data access control group \nsince acknowledgement of a policy is a condition for this data download.")
        print("\nRequires registration/manual download . . . :(")
        pass
    except:
        download_record['m']=download_record['m']+1
        os.remove(url.split('/')[len(url.split('/'))-1])
        pass
    

def DownloadCmip6(**kwargs):
    global startTime
    
    _var = kwargs.get('variable', None)
    _mod = kwargs.get('model', None)
    _exp = kwargs.get('experiment', None)
    _freq = kwargs.get('frequency', None)
    _realm = kwargs.get('realm', None)
    _node = kwargs.get('node', None)
    _check = kwargs.get('check', None)
    rlzn = kwargs.get('rlzn', None)
    year = kwargs.get('year', None)
    path = kwargs.get('path', None)
    skip = kwargs.get('skip', None)
    cr = kwargs.get('cr', None)

    # multi-thread kwarg
    multi = kwargs.get('multi', False)
    workers = kwargs.get('workers', None)
    
    # data range select
    start_year = kwargs.get('start_year', None)
    end_year   = kwargs.get('end_year', None)
    
    search=SearchDB()
    if (_check == 'Yes') or (_check == 'yes'):
        search._set_check('Yes')
    else:
        search._set_check('No')
    if (_mod != None):
            try:
                search.model=_mod
            except ValueError as ve:
                print(color.LRED+"\n<<No options available.>>\n\nPlease make sure "+str(_mod)+" exists."+color.END)
                print(ve)
            except Exception as ee:
                print('\nDid you mean any of the above?')
                print(ee)
    if (_exp != None):
        try:
            search.experiment=_exp
        except ValueError as ve:
            print(color.LRED+"\n<<No options available.>>\n\nPlease make sure "+str(_exp)+" exists."+color.END)
            print(ve)
        except Exception as ee:
            print('\nDid you mean any of the above?')
            print(ee)
    if (_var != None):
        try:
            search.variable=_var
        except ValueError as ve:
            print(color.LRED+"\n<<No options available.>>\n\nPlease make sure "+str(_var)+" exists."+color.END)
            print(ve)
        except Exception as ee:
            print('\nDid you mean any of the above?')
            print(ee)
    if (_freq != None):
        try:
            search.frequency=_freq
        except ValueError as ve:
            print(color.LRED+"\n<<No options available.>>\n\nPlease make sure "+str(_freq)+" exists."+color.END)
            print(ve)
        except Exception as ee:
            print('\nDid you mean any of the above?')
            print(ee)
    if (_realm != None):
        try:
            search.realm=_realm
        except ValueError as ve:
            print(color.LRED+"\n<<No options available.>>\n\nPlease make sure "+str(_realm)+" exists."+color.END)
            print(ve)
        except Exception as ee:
            print('\nDid you mean any of the above?')
            print(ee)
    if (_node != None):
        try:
            search.node=_node
        except ValueError as ve:
            print(color.LRED+"\n<<No options available.>>\n\nPlease make sure "+str(_node)+" exists."+color.END)
            print(ve)
        except Exception as ee:
            print('\nDid you mean any of the above?')
            print(ee)
    
    print("\nFinding server . . .")
    links = search.get_links(0)
        
    if (links == []):
        print('\n'+color.LRED+'<<Invalid search items!>>'+color.END)
        print('\n'+color.UNDERLINE+color.BOLD+'TIPS 1:'+color.END+' Use the check (-c) argument to check your inputs.'+color.END)
        print('\n'+color.UNDERLINE+color.BOLD+'TIPS 2:'+color.END+' Use CMIP6DB module to look for currently available '
              'models/experiments/variables and so on . . .')
        raise SystemExit
    
    
    if (start_year!=None and end_year != None):
        info = search.get_info()
        yr_links=[]
        interested_years=getTimeRange(start_year, end_year, info.year)
        for item in interested_years:
            for link in links:
                if '_'+str(item) in link:
                    yr_links.append(link)
        links = yr_links
    
    if (skip!=None):
        links=_get_skipped_links(links,skip)
    
    unused_links=[]    
    if (rlzn != None):
        all_rlzn = _realizations(links)._all_realizations()
        new_links = _get_rlzn_links(rlzn,all_rlzn,links)
        links=new_links
    
    if (cr!=None):
        info = search.get_info()
        exps = info.exp
        ers=[]
        for i in range(len(exps)):
            ers1 = [s for s in links if exps[i] in s]
            r1 = _realizations(ers1)._all_realizations()
            if i==1:
                ers2 = [s for s in links if exps[i-1] in s]
                r2 = _realizations(ers2)._all_realizations()
            elif i>1:
                r2 = ers
            else:
                ers2 = ers1
                r2 = _realizations(ers2)._all_realizations()
            ers = list(set(r1) & set(r2))
        ers=['_r'+str(s)+'i' for s in ers]
        links=[s for s in links if any(xs in s for xs in ers)]
    
    if (path == None):
        dir_path = _dir_path()._make_dir()
    else:
        dir_path = Path(path)
    
    if not os.path.isdir(dir_path):
        print('creating ', dir_path)
        os.makedirs(str(dir_path))
        
    os.chdir(dir_path) 

    download_record = {
        'n': 0,
        'm': 0,
        'manual': 0
    }

    passed_urls=[]

    # ! multi-thread
    if multi:
        pool = ThreadPoolExecutor(max_workers=workers)
        params = [(url, dir_path, passed_urls, download_record) for url in links]

        pool.map(single_download, params)

        pool.shutdown(wait=True, cancel_futures=False)
    else:
        for url in links:
            single_download(url, dir_path, passed_urls, download_record)
    
    n = download_record['n']
    m = download_record['m']
    manual = download_record['manual']
        
    print("\nFinished downloading.")
    print("\n\nDownloaded ",n," out of ",n+m," files.")
    if (m>0):
        print("\n\nRe-run the script for the missing files.")
    if (manual>0):
        print("\n\n",manual," files require an ESGF account/openID.")
        print("\nwget script created for these files!\nUse it with your openid/password >> 'wget_script -H'")
        with HidePrint():
            original_links = search.get_links(1)
        unused_links=list(set(original_links)-set(links))
        _manual_wget(passed_urls,unused_links)
