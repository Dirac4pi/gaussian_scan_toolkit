'''
This script is used to plot (multi) electronic energy
curve(s) based on Gaussian scan calculation.
coding:UTF-8
env:vis2c
'''

from os import path
from numpy import linspace
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import sys

har2kcal = 627.51
start = [2.8, 1.45, 1.45]      # Starting value
step = [-0.1, 0.05, 0.05]       # Step size
color = ['#005ba0', '#00978d', '#BF1D2D']
label = ['scan1', 'scan2', 'scan3']

xlabel = 'C-C length (Angstrom)'
ylabel = 'Energy (kcal/mol)'

#-------------------------------------------------------------------------------
def scanplot(scanout:str, iscan) -> None:
  '''
  Perform single-point splitting for Gaussian rigid / relaxed scanning
  --
  :scanout: Gaussian scan output file
  :iscan: Serial number of the scan output file
  '''
  global har2kcal
  # check input
  if not (scanout.endswith('.log') or scanout.endswith('.out')):
    raise RuntimeError('Unrecognized scan output file')
  if not path.exists(scanout):
    print(f'Error: scan output file {scanout} not found')
    sys.exit(1)
  # process scan output file
  scantype = 'none'
  with open(scanout,'r') as f:
    while True:
      line = f.readline()
      if not line:
        break
      if 'The following ModRedundant' in line:
        scantype = 'modredundant'
        print(f'{iscan}: scantype = modredundant')
        break
      elif 'scan the potential surface' in line:
        scantype = 'scan'
        print(f'{iscan}: scantype = scan')
        break
  with open(scanout, 'r') as f:
    lines = f.readlines()
  if scantype == 'none':
    raise RuntimeError('Unrecognized scan type')
  elif scantype == 'scan':
    ene = []
    for i in range(len(lines)):
      if 'SCF Done:' in lines[i]:
        line = lines[j]
        ene.append(float(line[line.find("=")+1:line.find("A.U.")].strip()))
  elif scantype == 'modredundant':
    ene = []
    for i in range(len(lines)):
      if 'Optimized Parameters' in lines[i]:
        j = i
        while j > 1:
          if 'SCF Done:' in lines[j]:
            line = lines[j]
            ene.append(float(line[line.find("=")+1:line.find("A.U.")].strip()))
            break
          j = j - 1
  if len(ene) == 0:
    print(f'{iscan}: no energy info found')
    sys.exit(1)
  else:
    print(f'{iscan}: {len(ene)} energy found')
  # process energy
  ZERO = ene[0]
  for i in range(len(ene)):
    ene[i] = (ene[i] - ZERO) * har2kcal
  # plot
  count = linspace(start[iscan], start[iscan]+len(ene)*step[iscan], len(ene))
  count_smooth = linspace(start[iscan], start[iscan]+len(ene)*step[iscan], 100)
  if step[iscan] > 0:
    ene_smooth = make_interp_spline(count, ene)(count_smooth)
  else:
    rcount = count[::-1]
    rcount_smooth = count_smooth[::-1]
    rene = ene[::-1]
    rene_smooth = make_interp_spline(rcount, rene)(rcount_smooth)
    ene_smooth = rene_smooth[::-1]
  plt.plot(count_smooth, ene_smooth, linewidth=2, \
           color=color[iscan], label=label[iscan])


#===============================================================================
if __name__ == "__main__":
  if len(sys.argv) == 2:
    scan_out1 = sys.argv[1]
    scanplot(scan_out1, 0)
  elif len(sys.argv) == 3:
    scan_out1 = sys.argv[1]
    scan_out2 = sys.argv[2]
    scanplot(scan_out1, 0)
    scanplot(scan_out2, 1)
  elif len(sys.argv) == 4:
    scan_out1 = sys.argv[1]
    scan_out2 = sys.argv[2]
    scan_out3 = sys.argv[3]
    scanplot(scan_out1, 0)
    scanplot(scan_out2, 1)
    scanplot(scan_out3, 2)
  else:
    print("Usage: python scanplot.py <scan_out1> (<scan_out2>) (<scan_out3>)")
    sys.exit(1)
  plt.legend()
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.show()