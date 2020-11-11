from simple.units.safe_units import natural_unit as nu
from simple.units.safe_units import *
a = nu(4,1)
b = nu(6,'energy')/eV
c = nu(4,2)

print(eV.massdimension,c.massdimension, b)
print(a+b*4.3*eV)
print(c/a+b*eV)

print(5**(year/(T*second)))

print ( (year + 0*second) * to (second))

