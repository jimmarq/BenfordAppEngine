# Test benford's law against your c:\windows directory
# (c)Twm Davies 2007

import math
def PFirstDigit(d):
    """Use benfords law to determine probility of the digit d"""
    return math.log(1.0+ 1.0/float(d)) / math.log(10)

def naturalness(sample):
    firstdigits = [int(str(li)[0]) for li in sample]

    sumdifference = 0
    r = range(1,10)
    for n in r:
        digitDistribution = float(firstdigits.count(n))/ len(sample)
        digitDifference =  abs(PFirstDigit(n)-digitDistribution)
        print "%d\t%.2f\t%.2f\t%.2f" % (n,PFirstDigit(n), digitDistribution, digitDifference)
        sumdifference = sumdifference + digitDifference
    return sumdifference

import os

scanpath = "c:\\windows"

dirs = os.listdir(scanpath)

filesizes = []

for file in dirs:
    try:
        size = os.path.getsize(scanpath + "\\" + file)
        if(size):
            filesizes.append(size)
    except: #this filters out directories (since calling getsize on dirs raises an exception)
        pass

overall = naturalness(filesizes)
print overall

