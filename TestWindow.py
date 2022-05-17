from math import ceil
from numpy import float16, int16


var1 = float16(10)
var2 = float16(0.01)

nvar1 = float16(var1/(2**15))
nvar2 = int16(0.00512/(nvar1*var2))

#print(2**16,end='\t')
print(var1,end='\t')
print(var2,end='\t')
print(nvar1,end='\t')
print(nvar2,end='\t')
print(round(nvar1,1),end='\t')
print(round(nvar2,2),end='\t')
print(ceil(nvar2),end='\t')
print(int16(nvar2))



