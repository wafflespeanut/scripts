execfile("Oracle.py")
import os,sys

# A server knows the key. Our job is to find the key by sending & receiving packets...

def test(File='CBC.txt'):   # Usage: `python Padding.py <filename>`
    with open(File,'r') as file: data=file.readlines()
    data=data[0]; print '\nTEST:',data
    ctext=[(int(data[i:i+2],16)) for i in range(0,len(data),2)]
    print "\nCTEXT:",ctext,'\n'
    connect(); print '\nSending ciphertext...\n'; rc=send(ctext,3)
    print "Oracle returned: %d\n" % rc; disconnect()

if len(sys.argv)>=2: test(sys.argv[1])
else: test()
