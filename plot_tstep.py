#!/usr/bin/env python3

from mpl_toolkits.basemap import Basemap 
from netCDF4 import Dataset, date2index, num2date
import datetime as dt
import matplotlib.pyplot as plt 
import numpy as np
import matplotlib 
import ipdb
#import cmocean as cm

matplotlib.rcParams['mathtext.default']='regular'
matplotlib.rcParams['legend.frameon']='True'
matplotlib.rcParams['figure.autolayout']='False'

_hs = {'vname':'hs','v_min':0, 'v_max':15, 'legend':r'$H_s(m)$',\
        'cmap':'YlGnBu_r'}
_tm = {'vname':'t','v_min':0, 'v_max':20, 'legend':r'$T_m(s)$', 'cmap':'PuBu_r'}
_dm = {'vname':'dir','v_min':0, 'v_max':359, 'legend':r'$\theta(^o)$',\
        'cmap':'twilight_shifted'}

_vars = {'hs':_hs,'tm':_tm,'dm':_dm}


def parse_time(str_time):
    date = dt.datetime.strptime(str_time, '%Y%m%d%H')
    return date

def read_file(i_fname, var, date):

    dt_file = Dataset(i_fname, 'r')

    idx_plt = date2index(date, dt_file['time'], select='nearest')
    dte_idx = num2date(idx_plt, dt_file['time'].units)

    if dte_idx != date:
        dte_beg = num2date(0, dt_file['time'].units)
        dte_end = num2date(dt_file['time'].size, dt_file['time'].units)

        print("*** Requested date: {}, nearest date found in file: {}."\
            .format(date.strftime('%Y%m%d%H'), dte_idx.strftime('%Y%m%d%H')))
        print("*** File starts at {} and ends at {}."\
            .format(dte_beg.strftime('%Y%m%d%H'), dte_end\
            .strftime('%Y%m%d%H')))


    lon = np.asarray(dt_file['longitude'][:])
    lat = np.asarray(dt_file['latitude'][:])

    data = np.asarray(dt_file[_vars[var]['vname']][idx_plt])
    dt_file.close()

    return  {'values':data,\
            'lon':lon,\
            'lat':lat,\
            'date':dte_idx}


def plot_data(data, out_dir, var):

    data['values'][np.where(data['values'] < 0)] = np.nan

    r_lon = data['lon'][1] - data['lon'][0]
    r_lat = data['lat'][1] - data['lat'][0]

    m = Basemap(projection='cyl', resolution='i', \
       llcrnrlon = data['lon'].min()-(r_lon/2), \
       llcrnrlat = data['lat'].min()-(r_lat/2), \
       urcrnrlon = data['lon'].max()+(r_lon/2), \
       urcrnrlat = data['lat'].max()+(r_lat/2))

#    m.bluemarble()
    m.fillcontinents(color='k', alpha=.4 ,zorder=3)
    m.drawcoastlines(color='k', linewidth=0.3,zorder=3)

    m.drawparallels(np.arange(-90., 100., 15), labels=[1,0,0,0], fontsize=8,\
        linewidth=.1)

    m.drawmeridians(np.arange(0., 370., 60), labels=[0,0,0,1], fontsize=8,\
        linewidth=.1)

    m.imshow(data['values'], vmin = _vars[var]['v_min'],\
        vmax = _vars[var]['v_max'], cmap = _vars[var]['cmap'])

    cbar = m.colorbar(label=_vars[var]['legend'])
    cbar.ax.tick_params(labelsize = 10)
    plt.title(data['date'].strftime('%Y%m%d%H'))
    plt.savefig(out_dir+_vars[var]['vname']+\
        data['date'].strftime('%Y%m%d%H')+'.png', dpi=200)

########################################### 
if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser( description='''Reads and plots coarse
            data from COWCLIP files.''' , usage='%(prog)s [options]')

    parser.add_argument('-v', required=True, metavar='var', help='''the
            variable to be plotted (required). Possible values are: \'hs\' 
            (significant wave height), \'tm\' (mean wave period), \'dm\' 
            (mean wave direction)''', choices = list(_vars.keys()),\
            default='h')

    parser.add_argument('-t', required=True, metavar='time', \
        help='''the time to plot in the \'YYYYMMDDHH\' form.''',\
        type = parse_time)

    parser.add_argument('-o',  metavar='out_path', default='./', \
        help='output path: (optional, default: ./)')

    parser.add_argument('-i',  metavar='input_file', \
        help='input file path. Ex. /mnt/ww3_outf_203006.nc')

    in_args = parser.parse_args()

    data = read_file(in_args.i, in_args.v, in_args.t) 

    plot_data(data, in_args.o, in_args.v)
