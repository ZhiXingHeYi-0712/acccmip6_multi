import argparse

import os

from acccmip6.access_cm import SearchCmip6
from acccmip6.download_dat import DownloadCmip6
from acccmip6.utilities.util import _check_list

def main():

    parser = argparse.ArgumentParser()
    
    parser.add_argument("-dir", help="Download directory.", default=None)
    parser.add_argument("-o","--output-options", help="S for 'Searching' or D for 'Downloading'. Use M to initiate the CMIP6DB module.", required=True)
    parser.add_argument("-m", help="Model names", default=None)
    parser.add_argument("-e", help="Experiment names", default=None)
    parser.add_argument("-v", help="Variable names", default=None)
    parser.add_argument("-f", help="Output frequency", default=None)
    parser.add_argument("-r", help="Output realm", default=None)
    parser.add_argument("-n", help="Output node", default=None)
    parser.add_argument("-rlzn", help="Select realization", default=None)
    parser.add_argument("-cr", help="Select common realizations", action='store_true', default=None)
    parser.add_argument("-yr", help="Select year, will be ignored when downloading, please use -starttime and -endtime instead.", default=None)
    parser.add_argument("-c", help="Checker: yes to check inputs", default=None)
    parser.add_argument("-desc", help="Description: yes to print out experiment description", default=None)
    parser.add_argument("-time", help="Description: yes to print out avalable time periods", default=None)
    parser.add_argument("-skip", help="Skip any item in your download", default=None)
    parser.add_argument("-serv", help="Set user-defined server", default=None)

    # add multi-thread
    parser.add_argument("-multi", help="Set using multi thread download, only available in downloading data. Set it True to enable.", default=False)
    parser.add_argument("-workers", help="Multi-thread download workders.", default=os.cpu_count())

    # add time range
    parser.add_argument("-starttime", help="data start year, only available in downloading.", default=None)
    parser.add_argument("-endtime", help="data end year, only available in downloading.", default=None)
	
    args = parser.parse_args()
    model = _check_list(args.m)
    experiment = _check_list(args.e)
    variable = _check_list(args.v)
    frequency = _check_list(args.f)
    realm = _check_list(args.r)
    node = _check_list(args.n)
    year = _check_list(args.yr)
    check = args.c
    rlzn = args.rlzn
    cr = args.cr
    desc = args.desc
    time = args.time
    out = args.output_options
    dl_dir = args.dir
    skipped = args.skip
    server = args.serv
    workers = int(args.workers)

    try:
        start_year = int(args.starttime)
        end_year   = int(args.endtime)
        if start_year > end_year:
            raise Exception('Start year should be earlier than end year.')
    except:
        start_year = None
        end_year = None

    multi_thread = args.multi == 'True'
    
    if (out == 'S'):
        SearchCmip6(model=model, experiment=experiment, variable=variable, frequency=frequency, realm=realm, check=check, desc=desc, year=year, time=time, rlzn=rlzn, node=node, skip=skipped, cr=cr, set_server=server)
    elif (out == 'M'):
        SearchCmip6(module='on', model=model, experiment=experiment, variable=variable, frequency=frequency, realm=realm, node=node)
    elif (out == 'D'):
        DownloadCmip6(model=model, experiment=experiment, variable=variable, frequency=frequency, realm=realm, check=check, path=dl_dir, rlzn=rlzn, node=node, skip=skipped, year=year, cr=cr, multi=multi_thread, workers=workers, start_year=start_year, end_year=end_year)
        
