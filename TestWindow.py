from math import ceil
import string
from numpy import char, float16, int16
import pigpio

ina226 = pigpio.pi()
testlist = [0xff,0xff]
ina226.i2c_write_i2c_block_data(0x40,0x5,testlist)

var1 = float16(10)
var2 = float16(0.01)
var3 = [0xff,0xff,0xff]

nvar1 = float16(var1/(2**15))
nvar2 = int16(0.00512/(nvar1*var2))

print(len(var3),end='\t')

print(var1,end='\t')
print(var2,end='\t')
print(nvar1,end='\t')
print(nvar2,end='\t')
print(round(nvar1,1),end='\t')
print(round(nvar2,2),end='\t')
print(ceil(nvar2),end='\t')
print(int16(nvar2))






