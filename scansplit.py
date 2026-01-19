'''
Perform single-point splitting for Gaussian16 rigid / relaxed scanning.
coding:UTF-8
env:base
'''

from os import path
import sys

elements = [         # (0 = ghost atom "Bq")
  "Bq", "H ", "He",  # 0-2
  "Li", "Be", "B ", "C ", "N ", "O ", "F ", "Ne",  # 3-10
  "Na", "Mg", "Al", "Si", "P ", "S ", "Cl", "Ar",  # 11-18
  "K ", "Ca", "Sc", "Ti", "V ", "Cr", "Mn", "Fe", \
  "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr",  # 19-36
  "Rb", "Sr", "Y ", "Zr", "Nb", "Mo", "Tc", "Ru", \
  "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I ", "Xe",  # 37-54
  "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", \
  "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu",  # 55-71
  "Hf", "Ta", "W ", "Re", "Os", "Ir", "Pt", "Au", \
  "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn",  # 72-86
  "Fr", "Ra", "Ac", "Th", "Pa", "U ", "Np", "Pu", \
  "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr",  # 87-103
  "Rf", "Db", "Sg", "Bh", "Hs", "Mt"  # 104-109
]

#-------------------------------------------------------------------------------
def isint(string: str) -> bool:
  '''
  Determine whether the string is an integer or not
  --
  :string: input string\n
  return: true/false
  '''
  try:
    int(string)
  except ValueError:
    return False
  else:
    return True

#-------------------------------------------------------------------------------
def loclabel(file_handle, label):
  """
  Find the line where the label first appears in file
  Returns (found, line) where found is boolean
  If found, file pointer is positioned at the line before the label
  """
  file_handle.seek(0)  # Always rewind
  for line_num, line in enumerate(file_handle):
    if label in line:
      # Move back one line so next read gets this line
      file_handle.seek(file_handle.tell() - len(line) - 1)
      return True, line_num
  return False, -1

#-------------------------------------------------------------------------------
def load_geom_scan(scanout:str):
  '''
  Find all geometry blocks in Gaussian rigid scan output file
  --
  :scanout: Gaussian scan output file
  '''
  global elements
  Natom = 0
  with open(scanout, 'r') as f:
    while True:
      line = f.readline()
      if not line:
        break
      if 'NAtoms=' in line:
        Natom = int(line.split()[1])
        break
  if Natom == 0:
    raise RuntimeError(f'No Natom found in {scanout}')
  else:
    print(f'{Natom} atoms found in molecule')
  scan = []
  with open(scanout, 'r') as f:
    iline = 0
    while True:
      line = f.readline()
      if not line:
        break
      iline += 1
      if 'Z-Matrix orientation:' in line:
        scan.append(iline+4)
  if len(scan) == 0:
    print('try Input orientation / Z-Matrix orientation / Standard orientation')
    sys.exit(1)
  with open(scanout, 'r') as f:
    lines = f.readlines()
  geom = [[] for _ in range(len(scan))]
  for i in range(len(scan)):
    j = scan[i]
    while j <= scan[i]+Natom-1:
      cod = elements[int(lines[j].split()[1])]+'   '
      cod = cod + \
      lines[j].split()[3]+'   '+lines[j].split()[4]+'   '+lines[j].split()[5]
      geom[i].append(cod)
      j += 1
  return geom

#-------------------------------------------------------------------------------
def load_geom_modredundant(scanout:str):
  '''
  Find all geometry blocks in Gaussian relaxed scan output file
  --
  :scanout: Gaussian scan output file
  '''
  global elements
  Natom = 0
  with open(scanout, 'r') as f:
    while True:
      line = f.readline()
      if not line:
        break
      if 'NAtoms=' in line:
        Natom = int(line.split()[1])
        break
  if Natom == 0:
    raise RuntimeError(f'No Natom found in {scanout}')
  else:
    print(f'{Natom} atoms found in molecule')
  scan = []
  with open(scanout, 'r') as f:
    iline = 0
    opted = False
    while True:
      line = f.readline()
      if not line:
        break
      iline += 1
      if 'Optimized Parameters' in line:
        opted = True
      if opted and 'Input orientation:' in line:
        opted = False
        scan.append(iline+4)
  if len(scan) == 0:
    print('try Input orientation / Z-Matrix orientation / Standard orientation')
    sys.exit(1)
  with open(scanout, 'r') as f:
    lines = f.readlines()
  geom = [[] for _ in range(len(scan))]
  for i in range(len(scan)):
    j = scan[i]
    while j <= scan[i]+Natom-1:
      cod = elements[int(lines[j].split()[1])]+'   '
      cod = cod + \
      lines[j].split()[3]+'   '+lines[j].split()[4]+'   '+lines[j].split()[5]
      geom[i].append(cod)
      j += 1
  return geom

#-------------------------------------------------------------------------------
def scansplit(scanout:str, gjftemp:str) -> None:
  '''
  Perform single-point splitting for Gaussian rigid / relaxed scanning
  --
  :scanout: Gaussian scan output file
  :gjftemp: Gaussian single-point template file
  '''
  # check input 
  if scanout.endswith('.log') or scanout.endswith('.out'):
    if gjftemp.endswith('.gjf'):
      scanout = scanout
      gjftemp = gjftemp
    else:
      raise RuntimeError('Unrecognized input file')
  elif scanout.endswith('.gjf'):
    if gjftemp.endswith('.log') or gjftemp.endswith('.out'):
      temp = scanout
      scanout = gjftemp
      gjftemp = temp
    else:
      raise RuntimeError('Unrecognized input file')
  else:
      raise RuntimeError('Unrecognized input file')
  if not path.exists(scanout):
    print(f'Error: scan output file {scanout} not found')
    sys.exit(1)
  if not path.exists(gjftemp):
    print(f'Error: GJF template file {gjftemp} not found')
    sys.exit(1)
  print(f'scan output file: {scanout}')
  print(f'GJF template file: {gjftemp}')
  # load gjftemp
  with open(gjftemp, 'r') as f:
    GJFlines = [line.rstrip('\n') for line in f]
  for i in range(len(GJFlines)):
    split = GJFlines[i].split()
    if len(split) == 2 and isint(split[0]) and isint(split[1]): # charge spin
      icod = i + 1
  # process scan output file
  scantype = 'none'
  with open(scanout,'r') as f:
    while True:
      line = f.readline()
      if not line:
        break
      if 'The following ModRedundant' in line:
        scantype = 'modredundant'
        break
      elif 'scan the potential surface' in line:
        scantype = 'scan'
        break
  if scantype == 'scan':
    print('scantype = scan')
    geom = load_geom_scan(scanout)
  elif scantype == 'modredundant':
    print('scantype = modredundant')
    geom = load_geom_modredundant(scanout)
  else:
    raise RuntimeError('Unrecognized scan type')
  if not geom:
    print("No geometry blocks found in scan output file")
    sys.exit(1)
  else:
    print(f"{len(geom)} geometrys found")
  # Generate input files for each geometry
  i = 1
  while i <= len(geom):
    if len(str(i)) == 1:
      filename = '000' + str(i)
    elif len(str(i)) == 2:
      filename = '00' + str(i)
    elif len(str(i)) == 3:
      filename = '0' + str(i)
    with open(filename+'.gjf', 'w') as f:
      f.write(f'%chk={filename}.chk\n')
      j = 1
      while j <= icod:
        f.write(GJFlines[j-1]+'\n')
        j += 1
      k = 1
      while k <= len(geom[i-1]):
        f.write(geom[i-1][k-1]+'\n')
        k += 1
      while j <= len(GJFlines):
        f.write(GJFlines[j-1]+'\n')
        j += 1
      f.write('\n')
      f.write('\n')
    i += 1
  print("All Gaussian input files have been generated in current folder")

#===============================================================================
if __name__ == "__main__":
  if len(sys.argv) != 3:
    print("Usage: python scansplit.py <scan_out_file> <template_gjf_file>")
    sys.exit(1)
  scansplit(sys.argv[1], sys.argv[2])