# Gaussian_Scan_Toolkit

&nbsp;&nbsp;&nbsp;&nbsp;There are several useful scripts for Gaussian
rigid/relaxed scan calculations.<br>

## scansplit.py

&nbsp;&nbsp;&nbsp;&nbsp;Inspired by the [SCANsplit program](http://sobereva.com/199)
developed by Sobereva, this script can be used to extract the structures from
all frames in the Gaussian rigid/relaxed scan output file and generate severial
single-point GJF files for each frame according to the GJF template. One can
customize the implicit solvent model in the GJF template or read the initial
wavefunction from %oldchk without worrying that they will be ignored. The script
could be useful if you need to analyze the evolution of electronic structure or
plot adiabatic potential energy surfaces of excited states, etc. Usage:
`python scansplit.py gjftemp.gjf scanout.out`, input order is irrelevant.<br>

## scanplot.py

&nbsp;&nbsp;&nbsp;&nbsp;Up to 3 Gaussian rigid/relaxed scanning curves can be
plotted on a single canvas for easier analysis and presentation. With simple
setup, it can produce **publishable-quality** images. Usage:
`python scanplot.py scanout1.log (scanout2.log) (scanout3.log)`.<br>

## apesplot.py

&nbsp;&nbsp;&nbsp;&nbsp;This script is used to plot the adiabatic potential
energy surfaces(APESs) of multiple excited states distinguished by spin
multiplicity, based on the Wigner-Eckart theorem(2 or 3 spin are reachable). It
should be used in conjunction with `scansplite.py`. With simple setup, it can
produce **publishable-quality** images. Usage: place all the Gaussian
single-point excited state calculation output files into the `apesplot.py`
directory，modify the scanning settings at the top of the `apesplot.py` (one can
also add the diabatic states and excitation wavelength), then run
`python apesplot.py`.<br>

## reverse.py

&nbsp;&nbsp;&nbsp;&nbsp;Sometimes it's necessary to perform a reverse scan and
plot in the forward way. In this case, `reverse.py` should be called before
plotting. Usage: place all the Gaussian single-point excited state calculation
output files into the `reverse.py` directory，then run `python reverse.py`.<br>
