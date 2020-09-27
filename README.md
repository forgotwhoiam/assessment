usage: plot_tstep.py [options]

Reads and plots coarse data from COWCLIP files.

optional arguments:
  -h, --help     show this help message and exit
  -v var         the variable to be plotted (required). Possible values are:
                 'hs' (significant wave height), 'tm' (mean wave period), 'dm'
                 (mean wave direction)
  -t time        the time to plot in the 'YYYYMMDDHH' form.
  -o out_path    output path: (optional, default: ./)
  -i input_file  input file path. Ex. /mnt/ww3_outf_203006.nc
