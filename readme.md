# Gaussian_Scan_Toolkit

&nbsp;&nbsp;&nbsp;&nbsp;There are several useful scripts for Gaussian
rigid/relaxed scan calculations.<br>

## scansplit.py

&nbsp;&nbsp;&nbsp;&nbsp;Inspired by the [SCANsplit program](http://sobereva.com/199)
developed by Sobereva, this script can be used to extract the structures from
all frames in the Gaussian rigid/relaxed scan output file and generate severial
single-point GJF files for each frame according to the GJF template. You can
customize the implicit solvent model in the GJF template or read the initial
wavefunction from %oldchk without worrying that they will be ignored. The script
could be useful if you need to analyze the evolution of electronic structure or
plot adiabatic potential energy surfaces of excited states, etc. Usage:
`python scansplit.py gjftemp.gjf scanout.out`, input order is irrelevant.<br>

## scanplot.py

&nbsp;&nbsp;&nbsp;&nbsp;Up to 3 Gaussian rigid/relaxed scanning curves can be
plotted on a single canvas for easier analysis and presentation. You may also
customize the plotting if needed. Usage:
`python scanplot.py scanout1.log (scanout2.log) (scanout3.log)`.<br>

## apesplot.py

&nbsp;&nbsp;&nbsp;&nbsp;This script is used to plot the adiabatic potential
energy surfaces(APES) of multiple excited states distinguished by spin
multiplicity. (Based on the Wigner-Eckart theorem, at most 3 spin states are
reachable). It should be used in conjunction with scansplite.py. Usage:
place all the Gaussian single-point excited state calculation output files that
you are interested in into the same directory as apesplot.py and then
`python apesplot.py`.<br>
